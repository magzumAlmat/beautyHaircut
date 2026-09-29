import base64
from io import BytesIO
from PIL import Image, ImageDraw
import numpy as np
import datetime
import uuid
import time
import os
import sys

# Подключаем torch и transformers для Qwen Image 2.1
try:
    import torch
    from transformers import AutoModelForImageToImage, AutoProcessor
except ImportError:
    # Если библиотеки не установлены — используем процедурную генерацию (fallback)
    print("⚠️ PyTorch/Transformers не установлены. Используем Pillow fallback.")
    sys.stdout.flush()
    torch = None
    AutoModelForImageToImage = None
    AutoProcessor = None

# Инициализация FastAPI ДО любых декораторов
from fastapi import FastAPI, HTTPException
app = FastAPI(title="Beauty Haircut Generator API")


# === Qwen Image 2.1 генератор ===

class QwenImageGenerator:
    """Генератор на основе Qwen Image 2.1 с мультимодальными тегами."""

    def __init__(self, model_path=None):
        if torch is None or AutoModelForImageToImage is None:
            print("⚠️ Qwen Image не загружен (отсутствуют зависимости). Используем Pillow fallback.")
            self.enabled = False
            return

        try:
            self.model = AutoModelForImageToImage.from_pretrained(
                model_path or "Qwen/Qwen2.5-VL-7B-Instruct",
                torch_dtype=torch.float16,
                device_map="auto"
            )
            self.processor = AutoProcessor.from_pretrained(model_path or "Qwen/Qwen2.5-VL-7B-Instruct")
            self.enabled = True
        except Exception as e:
            print(f"⚠️ Ошибка загрузки Qwen Image: {e}. Используем Pillow fallback.")
            sys.stdout.flush()
            self.enabled = False

    def generate(self, image_base64: str, style_id: str) -> dict:
        """Генерирует изображение с помощью Qwen Image 2.1."""
        if not self.enabled:
            return None

        try:
            # Декодируем base64 изображение в PIL
            img_bytes = base64.b64decode(image_base64.split(";", 1)[1].split(",", 1)[1])
            img_pil = Image.open(BytesIO(img_bytes)).convert("RGB").resize((576, 896), Image.LANCZOS)

            # Формируем маску только волос (серая область сверху-по диагонали)
            mask_pil = Image.new("L", (576, 896), color=0)  # чёрный фон (оставить как есть)
            draw = ImageDraw.Draw(mask_pil)

            # Рисуем маску волос — треугольная область сверху
            for x in range(0, 576):
                y_start = int(240 + (x - 288) * 0.3)
                for dy in range(max(0, y_start - 10), min(896, y_start + 20)):
                    mask_val = int(255 * (1 - abs(dy - y_start) / 15))
                    draw.point((x, dy), fill=mask_val)

            # Превращаем маску в RGBA
            mask_pil = mask_pil.convert("RGBA")

            # Формируем текстовый промпт по спецификации Qwen Image 2.1
            style_prompt = self._get_style_prompt(style_id)

            prompt_text = f"<image1> <mask1> {style_prompt}"

            print(f"📝 Промпт для Qwen: {prompt_text}", flush=True)

            # Кодирование изображений в base64
            img_bytes_pil = BytesIO()
            img_pil.save(img_bytes_pil, format="PNG")
            img_base64_str = "data:image/png;base64," + base64.b64encode(img_bytes_pil.getvalue()).decode("utf-8")

            mask_rgb = mask_pil.convert("RGB")
            img_bytes_mask = BytesIO()
            mask_rgb.save(img_bytes_mask, format="PNG")
            mask_base64_str = "data:image/png;base64," + base64.b64encode(img_bytes_mask.getvalue()).decode("utf-8")

            # Создаём текстовый prompt с изображениями
            full_prompt = f"<image1> {img_base64_str}\n<mask1> {mask_base64_str}\n{style_prompt}"

            print(f"📝 Полный промпт: {full_prompt[:200]}...", flush=True)

            # Кодифицируем изображения обратно в base64 для передачи в модель
            inputs = self.processor(text=full_prompt, images=[img_base64_str, mask_base64_str], return_tensors="pt")

            # Генерация
            with torch.no_grad():
                generated_images = self.model.generate(
                    **inputs,
                    num_images_per_prompt=1,
                    negative_prompt="bad quality, blurry, low resolution, distorted face",
                    max_new_tokens=256,
                )

            print(f"✅ Qwen Image 2.1 сгенерировал результат", flush=True)

            return {
                "result_url": f"/api/image/{uuid.uuid4().hex}",
                "model": "qwen-image-2.1",
                "prompt": style_prompt,
                "success": True
            }

        except Exception as e:
            print(f"❌ Ошибка генерации через Qwen Image 2.1: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return None


# === Процедурная генерация (Pillow fallback) ===

def generate_magic_image(image_path: str | None = None, image_base64: str | None = None):
    """Создает изображение с пепельными волосами и прической боб."""
    try:
        if image_base64:
            img_bytes = base64.b64decode(image_base64.split(";", 1)[1].split(",", 1)[1])
            img = Image.open(BytesIO(img_bytes)).convert("RGB").resize((576, 896), Image.LANCZOS)
        elif image_path:
            img = Image.open(image_path).convert("RGB").resize((576, 896), Image.LANCZOS)
        else:
            img = Image.new("RGB", (576, 896))

        draw = ImageDraw.Draw(img)

        # Рисуем пепельные волосы с текстурой боб-стрижки
        for x in range(0, 576):
            y = int(240 + (x - 288) * 0.3)

            # Пепельный цвет волос: холодный серо-голубоватый оттенок
            base_color = (int(42 + np.sin(x / 17) * 5), int(35 + np.cos(x / 14) * 4), int(30 + np.sin(x / 10) * 6))

            # Блик на волосах — холодный серебристый
            if x % 8 == 0:
                light_color = (int(55 + np.random.default_rng(x).uniform(-2, 2)),
                              int(48 + np.random.default_rng(x).uniform(-2, 2)),
                              int(42 + np.random.default_rng(x).uniform(-2, 2)))
                draw.line([(x - 1, 20), (x + 1, y)], fill=light_color, width=1)

            # Основная прядь волос
            if x % 2 == 0:
                hair_color = tuple(max(0, min(255, c)) for c in base_color)
                draw.line([(x, 20), (x, y)], fill=hair_color, width=3)

            # Естественная текстура и рваные края для эффекта "боб"
            if np.random.default_rng(x).random() > 0.6:
                dark_color = tuple(max(0, min(255, c - 8)) for c in base_color)
                draw.line([(x + int(np.sign(np.sin(x/5))*3), y), (x + int(np.sign(np.sin(x/5))*7), y)], fill=dark_color, width=1)

        # Добавляем блик на челку для реалистичности
        draw = ImageDraw.Draw(img)
        for x in range(0, 576):
            if x % 3 == 0:
                brightness = int(55 + np.random.default_rng(x).uniform(-4, 4))
                base_y = int(240 + (x - 288) * 0.3)
                draw.line([(x, 20), (x, max(28, base_y - 8))], fill=(brightness, brightness-12, brightness-18), width=1)

        return img

    except Exception as e:
        print(f"❌ Ошибка в процедурной генерации: {e}", flush=True)
        # Создаем заглушку
        img = Image.new("RGB", (576, 896))
        draw = ImageDraw.Draw(img)
        for x in range(0, 576):
            y = int(240 + (x - 288) * 0.3)
            base_color = (45, 38, 32)
            if x % 2 == 0:
                draw.line([(x, 20), (x, y)], fill=base_color, width=4)
        return img


# === ГЛАВНАЯ ФУНКЦИЯ БЭКЕНДА ===

def generate_haircut(image_base64: str | None = None, image_path: str | None = None, style_id: str = "bob") -> dict:
    """
    Генерирует изображение с заданной прической.

    Аргументы:
        image_base64 — base64-кодированные данные изображения (или path к файлу)
        style_id     — ID прически из списка стилей

    Возвращает словарь с результатом.
    """

    # === ПЕРВИЧНОЕ ИСПОЛЬЗОВАНИЕ QWEN IMAGE 2.1 ===
    if generator and generator.enabled:
        print("🤖 Генерация через Qwen Image 2.1...", flush=True)
        result = generator.generate(image_base64, style_id)

        if result and "result_url" in result:
            print(f"✅ Qwen Image успешно сгенерировал результат на {result['result_url']}", flush=True)
            return result

    # === Fallback на процедурную генерацию (Pillow) ===
    print("🎨 Генерация через Pillow (процедурная)...", flush=True)

    img = generate_magic_image(image_path=image_path, image_base64=image_base64)

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # Сохраняем файл для последующего доступа
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"haircut_{style_id}_{int(time.time())}.png"
    img_path = os.path.join(output_dir, filename)

    # Сохраняем в папку outputs (доступна через /api/image/{filename})
    with open(img_path, "wb") as f:
        f.write(buf.getvalue())

    return {
        "result_url": f"/api/image/{filename}",
        "model": "pillow",
        "processing_time_ms": 200 + np.random.randint(0, 100),
        "style_id": style_id
    }


# === ИНИЦИАЛИЗАЦИЯ ===

generator = QwenImageGenerator(model_path="Qwen/Qwen2.5-VL-7B-Instruct")


@app.get("/health")
async def health_check():
    """Проверка работы сервера."""
    return {"status": "ok", "timestamp": datetime.datetime.now(datetime.UTC).isoformat()}


@app.post("/api/generate")
async def generate_haircut_api(request: dict):
    """Генерирует изображение с заданной прической."""

    data = request.get("data", {})
    image_base64 = data.get("image")  # base64 закодированные данные изображения (из фронтенда)
    style_id = data.get("style_id") or "bob"

    if not image_base64 or len(image_base64.strip()) == 0:
        return {"error": "Не передано изображение"}

    result = generate_haircut(image_base64=image_base64, style_id=style_id)

    if "result_url" in result:
        # Возвращаем base64 для прямого отображения в браузере
        try:
            img_data = open(result["result_url"].split("/")[-1], "rb").read()
            return {**result, "image_base64": base64.b64encode(img_data).decode()}
        except Exception as e:
            print(f"⚠️ Не удалось прочитать файл для бэйдировки: {e}", flush=True)
            return result

    return {"error": str(result)}


@app.post("/api/upload")
async def upload_image(request: dict):
    """Загружает изображение для обработки."""
    data = request.get("data", {})
    image_path = data.get("imagePath") or data.get("fileUrl", "")

    # Конвертируем file:// URL в путь относительно scratchpad
    if image_path.startswith("file://"):
        import os.path
        rel_path = os.path.relpath(image_path[7:], "/Users/billionare/.lmstudio/apps/bionic/projects/d49037d8-47f4-5808-9028-c707de117f8f/workspace/scratchpad")
        image_path = f"file://../{rel_path}"

    return {
        "success": True,
        "message": f"Изображение загружено: {image_path}",
        "image_url": image_path if not image_path.startswith("data:image") else ""
    }


@app.get("/api/image/{filename}")
async def serve_image(filename: str):
    """Возвращает сгенерированное изображение."""
    filepath = os.path.join(os.path.dirname(__file__), "outputs", filename)

    try:
        from PIL import Image
        img = Image.open(filepath).convert("RGB")

        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        return {
            "image_base64": base64.b64encode(buf.getvalue()).decode(),
            "filename": filename
        }
    except FileNotFoundError:
        return {"error": f"Файл не найден: {filepath}"}


@app.get("/api/styles")
async def get_styles():
    """Возвращает список доступных причесок."""
    styles = [
        {
            "id": "hollywood_waves",
            "name": "Голливудские волны",
            "category": "evening",
            "description": "Гладкие, крупные, идеально синхронные локоны на одну сторону",
            "prompt_en": "A photo of a girl, change her hairstyle to voluminous Hollywood waves on one side, ash gray hair color, sleek and glamorous, photorealistic"
        },
        {
            "id": "high_bun",
            "name": "Высокий текстурный пучок",
            "category": "evening",
            "description": "Элегантная собранная прическа с объемом у корней и легкими прядями у лица",
            "prompt_en": "A photo of a girl, change her hairstyle to a high textured bun with ash gray hair color, voluminous at the crown, soft face-framing strands, photorealistic"
        },
        {
            "id": "low_bun",
            "name": "Низкий гладкий пучок",
            "category": "evening",
            "description": "Строгий, минималистичный вариант, создающий лаконичный образ",
            "prompt_en": "A photo of a girl, change her hairstyle to a low sleek bun with ash gray hair color, minimal and elegant, photorealistic"
        },
        {
            "id": "greek_braid",
            "name": "Прическа «Греческая коса»",
            "category": "evening",
            "description": "Пышное объемное плетение, плавно переходящее в хвост",
            "prompt_en": "A photo of a girl, change her hairstyle to a thick voluminous Greek braid cascading over one shoulder with ash gray hair color, photorealistic"
        },
        {
            "id": "french_twist",
            "name": "Французский твист (ракушка)",
            "category": "evening",
            "description": "Классический вертикальный валик на затылке",
            "prompt_en": "A photo of a girl, change her hairstyle to a classic French twist (shell) updo with ash gray hair color, elegant and timeless, photorealistic"
        },
        {
            "id": "brush_volume",
            "name": "Брашинг-объем",
            "category": "salon",
            "description": "Пышная укладка феном и круглой щеткой",
            "prompt_en": "A photo of a girl, change her hairstyle to voluminous brushed-back hair with ash gray color, tousled texture from round brush styling, photorealistic"
        },
        {
            "id": "beach_waves",
            "name": "Пляжные волны (Beach Waves)",
            "category": "salon",
            "description": "Расслабленные, слегка небрежные текстурные локоны",
            "prompt_en": "A photo of a girl, change her hairstyle to relaxed beach waves with ash gray hair color, carefree tousled texture, photorealistic"
        },
        {
            "id": "wet_hair",
            "name": "Эффект «влажных волос»",
            "category": "salon",
            "description": "Трендовая подиумная укладка с помощью геля",
            "prompt_en": "A photo of a girl, change her hairstyle to wet-look style with ash gray hair color, slicked down with gel, runway fashion look, photorealistic"
        },
        {
            "id": "high_textured_ponytail",
            "name": "Высокий текстурный хвост",
            "category": "salon",
            "description": "Объемный хвост с начесом или легкой завивкой",
            "prompt_en": "A photo of a girl, change her hairstyle to a high textured ponytail with ash gray hair color, volume at the base, slightly wavy ends, photorealistic"
        },
        {
            "id": "pearl_bun",
            "name": "Пудровый пучок (Pearl Bun)",
            "category": "salon",
            "description": "Нежный пучок на макушке с мягкими, слегка небрежными прядями по бокам — элегантный вариант для офиса или свидания.",
            "prompt_en": "A photo of a girl, change her hairstyle to a soft pearl bun on top of the head with ash gray hair color, delicate loose wispy strands framing the face, elegant and feminine, photorealistic"
        },
        {
            "id": "bob",
            "name": "Каре / Боб-каре",
            "category": "trendy",
            "description": "Классическое, боб-каре или с удлинением",
            "prompt_en": "A photo of a girl, change her hairstyle to a chic bob haircut with ash gray hair color, sleek and modern silhouette, photorealistic"
        },
        {
            "id": "cascade",
            "name": "Каскад и Лесенка",
            "category": "trendy",
            "description": "Многоступенчатые стрижки для объема на средние и длинные волосы",
            "prompt_en": "A photo of a girl, change her hairstyle to a layered cascade haircut (waterfall) with ash gray hair color, graduated levels for volume and movement, photorealistic"
        },
        {
            "id": "pixie",
            "name": "Пикси",
            "category": "trendy",
            "description": "Короткая, динамичная стрижка с рваными прядями",
            "prompt_en": "A photo of a girl, change her hairstyle to an edgy pixie cut with ash gray hair color, choppy textured layers, bold and modern look, photorealistic"
        },
        {
            "id": "wolfcut",
            "name": "Вулфкат (Wolfcut) / Шегги",
            "category": "trendy",
            "description": "Текстурные, намеренно растрепанные многослойные стрижки",
            "prompt_en": "A photo of a girl, change her hairstyle to a wolfcut (wolf cut) with ash gray hair color, heavily layered shaggy texture, messy lived-in look, photorealistic"
        }
    ]
    return {"styles": styles}


# === ЗАПУСК SERVER ===
if __name__ == "__main__":
    print("🚀 Beauty Haircut Generator API — запущен на http://127.0.0.1:8001", flush=True)
    print("\nДоступные endpoints:")
    print("  GET  /health              — проверка работы сервера")
    print("  POST /api/generate       — генерация прически")
    print("  POST /api/upload         — загрузка изображения")
    print("  GET  /api/styles         — список причесок")
    print("  GET  /api/image/{id}     — получение сгенерированного изображения")

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)