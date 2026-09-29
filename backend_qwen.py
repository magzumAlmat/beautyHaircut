"""
Qwen Image-to-Image API сервер с использованием gradio как веб-интерфейс.
Позволяет вызывать Qwen Image 2.1 через простой HTTP endpoint.
"""

import asyncio, logging, sys, tempfile
from pathlib import Path

try:
    from transformers import AutoModelForImageToImage, AutoProcessor, BitsAndBytesConfig
except ImportError as e:
    print(f"⚠️ Требуется установить: {e}")
    print("   pip install transformers torch huggingface_hub")
    sys.exit(1)

from PIL import Image
import io
import tempfile

# Путь к модели Qwen Image 2.1 (Image-to-Image)
MODEL_PATH = "./models/qwen-image-v1.5"
PORT = 8080

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def generate_image(image_path_or_bytes: bytes, prompt: str, output_path: Path):
    """Генерирует изображение с помощью Qwen Image 2.1."""
    
    if not Path(MODEL_PATH).exists():
        raise FileNotFoundError(
            f"Модель не найдена в {MODEL_PATH}. "
            f"Скачайте её через: huggingface-cli download Qwen/Qwen2.5-Image-VL-Instruct --local-dir {MODEL_PATH}"
        )

    try:
        from transformers import AutoModelForImageToImage, AutoProcessor, BitsAndBytesConfig
        
        logger.info(f"Загрузка модели из {MODEL_PATH}...")
        
        # Конфигурация для квантованной загрузки (меньше памяти)
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=False,
        )

        model_path_str = str(MODEL_PATH) if not MODEL_PATH.exists() else None
        
        processor = AutoProcessor.from_pretrained(MODEL_PATH)
        
        # Используем float16 для ускорения
        device_map = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Используем устройство: {device_map}")

        model = AutoModelForImageToImage.from_pretrained(
            MODEL_PATH,
            torch_dtype=torch.float16,
            device_map="auto",
            quantization_config=bnb_config if torch.cuda.is_available() else None,
        )

        logger.info("✅ Модель загружена!")

    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки модели: {e}")


async def generate_stream(image_url_or_path: str, prompt: str):
    """Генерирует изображение с Qwen Image 2.1 асинхронно."""
    import requests
    
    # Если передан URL — скачиваем картинку
    if image_url_or_path.startswith("http"):
        response = requests.get(image_url_or_path)
        response.raise_for_status()
        img_bytes = response.content
    else:
        with open(image_url_or_path, "rb") as f:
            img_bytes = f.read()

    # Сохраняем временный файл для обработки
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
        tmp_img.write(img_bytes)
        tmp_img_path = Path(tmp_img.name)

    try:
        # Загружаем модель один раз (глобально, если нужно кэшировать)
        from transformers import AutoModelForImageToImage, AutoProcessor
        
        if not hasattr(generate_image, "_model"):
            generate_image._processor = AutoProcessor.from_pretrained(MODEL_PATH)
            generate_image._model = AutoModelForImageToImage.from_pretrained(
                MODEL_PATH, torch_dtype=torch.float16, device_map="auto",
            )

        processor = getattr(generate_image, "_processor")
        model = getattr(generate_image, "_model")

        # Конвертируем в PIL Image
        img_pil = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        prompt_text = f"{prompt} photorealistic, high detail, 8k resolution, full body"

        inputs = processor(
            text=prompt_text,
            images=img_pil,
            return_tensors="pt",
        ).to(model.device)

        logger.info(f"Генерация: {prompt[:100]}...")

        with torch.no_grad():
            generated_images = model.generate(
                **inputs,
                num_images_per_prompt=1,
                negative_prompt="bad quality, blurry, distorted, deformed hands, bad anatomy, watermark, text",
                max_new_tokens=256,
                width=1024,
                height=1024,
            )

        # Преобразуем в PIL Image
        generated_image = Image.fromarray(generated_images[0].cpu().numpy())

        logger.info("✅ Генерация завершена!")

        return generated_image.convert("RGB")

    except Exception as e:
        logger.error(f"Ошибка генерации: {e}")
        raise


def main():
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import FileResponse, StreamingResponse
    from PIL import Image
    import io

    app = FastAPI(title="Qwen Image 2.1 API", docs_url="/docs")

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.post("/generate")
    async def generate_endpoint(
        image: str,
        prompt: str = "Change hair color to ash gray and style with bob haircut",
        output_format: str = "png"
    ):
        """
        Генерирует изображение через Qwen Image 2.1.

        Args:
            image: URL изображения или base64-encoded PNG/JPG/WebP.
            prompt: Текстовый промпт (например, "ash gray bob haircut").
            output_format: формат вывода ("png" или "webp").
        """
        logger.info(f"POST /generate — image={image[:50] if len(image) > 50 else image}, prompt={prompt}")

        try:
            # Если URL начинается с data:image — это base64
            is_base64 = image.startswith("data:image")
            
            if is_base64:
                import base64, mimetypes
                mime_type = "image/png"
                if "," in image:
                    mime, _ = image.split(",", 1)
                    mime_type = mime.strip()
                
                img_bytes = base64.b64decode(image.split(",", 1)[1])
            else:
                # Пробуем как URL или локальный файл
                try:
                    response = requests.get(image, timeout=30)
                    response.raise_for_status()
                    img_bytes = response.content
                    mime_type = "image/png"
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Не удалось загрузить изображение: {e}")

            # Проверяем тип изображения
            if not mime_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="Поддерживаются только изображения")

            # Создаём временный файл
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp.write(img_bytes)
                tmp_path = Path(tmp.name)

            try:
                result_img = await generate_stream(image_url_or_path=tmp_path, prompt=prompt)
                
                # Сохраняем результат
                with tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=False) as out_tmp:
                    result_pil = result_img.convert("RGB")  # удаляем альфа-канал если есть
                    result_pil.save(out_tmp.name, format=output_format.upper())
                    
                    return FileResponse(
                        out_tmp.name,
                        media_type=f"image/{output_format}",
                        headers={"X-Qwen-Version": "2.5-Image-VL"}
                    )

            finally:
                tmp_path.unlink(missing_ok=True)

        except Exception as e:
            logger.error(f"Ошибка генерации: {e!r}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/generate-async")
    async def generate_async_endpoint(
        image_url: str,
        prompt: str = "Change hair color to ash gray and style with bob haircut"
    ):
        """Асинхронный endpoint — генерирует изображение в фоне."""
        import threading
        
        result_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        
        def do_generate():
            try:
                img_pil = await generate_stream(image_url, prompt)
                img_pil.save(result_file.name, format="PNG")
            except Exception as e:
                logger.error(f"Ошибка в генерации: {e}")
        
        thread = threading.Thread(target=do_generate)
        thread.daemon = True
        thread.start()

        # Возвращаем статус "запущено", клиент получит файл позже (через polling или WebSocket)
        return {"status": "queued"}

    import uvicorn
    logger.info(f"🚀 Qwen Image 2.1 API запущен на http://0.0.0.0:{PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()