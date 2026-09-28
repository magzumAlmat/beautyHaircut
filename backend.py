"""Backend API for Hair Style Selector — Qwen Image 2.1 Integration."""

import base64, io as BytesIO, logging, random, re, time, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageEnhance, ImageChops
import numpy as np
import requests

# Конфигурация модели Qwen Image 2.1
QWEN_MODEL_PATH = "./models/qwen-image-v1.5"
QWEN_ENABLE = False  # Установите True после скачивания и установки модели
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Qwen Image 2.1 конфигурация
QWEN_CONFIG = {
    "base_url": "http://localhost:8080/v1",  # или адрес вашего сервера Qwen
    "api_key": "",  # если требуется авторизация
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def try_qwen_image_21(image_url: str, prompt: str) -> Optional[bytes]:
    """Попытка сгенерировать изображение через Qwen Image 2.1."""
    if not QWEN_ENABLE or not Path(QWEN_MODEL_PATH).exists():
        logger.info(f"Qwen Image 2.1 недоступна (путь: {QWEN_MODEL_PATH})")
        return None

    try:
        from transformers import AutoModelForImage2Image, AutoProcessor
        import torch
        
        processor = AutoProcessor.from_pretrained(QWEN_MODEL_PATH)
        model = AutoModelForImage2Image.from_pretrained(
            QWEN_MODEL_PATH,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        logger.info(f"Qwen Image 2.1 модель готова!")

        # Загрузить исходное изображение
        response = requests.get(image_url)
        if response.status_code != 200:
            raise Exception(f"Не удалось загрузить изображение: {response.status_code}")

        from PIL import Image as PILImage
        raw_image = PILImage.open(BytesIO(response.content)).convert("RGB")

        # Подготовить промпт
        prompt_text = f"{prompt} photorealistic, high detail, 8k resolution"

        inputs = processor(
            text=prompt_text,
            images=raw_image,
            return_tensors="pt",
        ).to(model.device)

        with torch.no_grad():
            generated_images = model.generate(
                **inputs,
                num_images_per_prompt=1,
                negative_prompt="bad quality, blurry, distorted, deformed hands, bad anatomy, watermark, text",
                max_new_tokens=256,
                width=1024,
                height=1024,
            )

        # Преобразовать в PIL Image
        generated_image = PILImage.fromarray(generated_images[0].cpu().numpy())

        logger.info("Qwen Image 2.1 генерация завершена успешно!")
        return generated_image.convert("RGB")

    except ImportError as e:
        logger.error(f"Требуется установить transformers и torch: {e}")
        raise
    except Exception as e:
        logger.error(f"Ошибка Qwen Image 2.1: {e!r}")
        return None


# Палитра цветов волос
HAIR_COLORS = {
    "ash_gray":       (168, 169, 173),
    "light_ash":      (192, 192, 200),
    "dark_gray":      (112, 112, 112),
    "platinum":       (225, 230, 235),
    "ebony_gray":     (90, 92, 94),
}

# 14 причесок
HAIRSTYLES = {
    "hollywood": {"name": "Голливудские волны", "desc": "Гладкие крупные локоны на одну сторону", "category": "вечерние"},
    "high_bun":  {"name": "Высокий текстурный пучок", "desc": "Элегантная собранная прическа с объемом у корней", "category": "вечерние"},
    "low_bun":   {"name": "Низкий гладкий пучок", "desc": "Строгий минималистичный вариант", "category": "вечерние"},
    "greek_braid":{"name": "Греческая коса", "desc": "Пышное объемное плетение переходящее в хвост", "category": "вечерние"},
    "french_twist":{"name": "Французский твист (ракушка)", "desc": "Классический вертикальный валик на затылке", "category": "вечерние"},
    "blowout":   {"name": "Брашинг-объем", "desc": "Пышная укладка феном и круглой щеткой", "category": "салонные"},
    "beach_waves":{"name": "Пляжные волны (Beach Waves)", "desc": "Расслабленные небрежные текстурные локоны", "category": "салонные"},
    "wet_hair":  {"name": "Эффект влажных волос", "desc": "Трендовая подиумная укладка с гелем", "category": "салонные"},
    "high_ponytail":{"name": "Высокий текстурный хвост", "desc": "Объемный хвост с начесом или легкой завивкой", "category": "салонные"},
    "straight_hair":{"name": "Идеально прямые волосы", "desc": "Вытянутые утюжком пряди с глянцевым блеском", "category": "салонные"},
    "bob":       {"name": "Каре / Боб-каре", "desc": "Классическое каре или боб с удлинением", "category": "стрижки"},
    "cascade":   {"name": "Каскад и Лесенка", "desc": "Многоступенчатые стрижки для объема на средние волосы", "category": "стрижки"},
    "pixie":     {"name": "Пикси", "desc": "Короткая динамичная стрижка с рваными прядями", "category": "стрижки"},
    "wolfcut":   {"name": "Вулфкат (Wolfcut) / Шегги", "desc": "Текстурные многослойные растрепанные стрижки", "category": "стрижки"},
}


class HairStyleGenerator:
    """Процедурная генерация причесок через PIL + numpy."""

    def __init__(self):
        self.STYLES = HAIRSTYLES
        logger.info("HairStyleGenerator инициализирован")

    def generate(self, img_path_or_base64: str, style_id: str, color: str) -> bytes:
        """Генерирует изображение с заданным стилем прически и цветом волос."""
        import time

        # 1. Попробовать Qwen Image 2.1
        prompt = self._get_prompt_for_style(style_id)
        
        qwen_result = try_qwen_image_21(img_path_or_base64, prompt)
        
        if qwen_result is not None:
            logger.info(f"✅ Qwen Image 2.1 успешно сгенерировал изображение для стиля: {style_id}")

            # Сохранить результат
            output_dir = OUTPUT_DIR / "qwen"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"{color}_{style_id}_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}.png"
            img_save_path = output_dir / filename
            
            qwen_result.save(img_save_path)
            logger.info(f"[QWEN] Сохранено в: {img_save_path}")

            return img_save_path.read_bytes()

        # 2. Fallback на процедурную генерацию через Pillow
        logger.warning("Falling back to procedural generation (Pillow)")
        return self._generate_with_pillow(img_path_or_base64, style_id, color)

    def _get_prompt_for_style(self, style_id: str) -> str:
        """Получает промпт для заданного стиля."""
        prompts = {
            "hollywood": "long wavy hair with Hollywood waves swept to one side",
            "high_bun": "elegant high textured bun hairstyle with volume at roots and loose strands framing the face",
            "low_bun": "strict low sleek bun hairstyle, minimalist style",
            "greek_braid": "voluminous thick braided hairstyle transitioning into a ponytail",
            "french_twist": "classic vertical roll bun (shell) on the back of the head",
            "blowout": "full volume blowout hairstyle with round brush styling",
            "beach_waves": "relaxed messy textured beach waves",
            "wet_hair": "trendy runway wet hair look with gel effect",
            "high_ponytail": "voluminous high ponytail with backcombing and light curls",
            "straight_hair": "perfectly straight sleek hair with glossy shine from flat iron",
            "bob": "classic bob haircut or long bob with layers",
            "cascade": "multi-layered cascade haircut for medium to long hair volume",
            "pixie": "short dynamic pixie cut with chunky textured bangs",
            "wolfcut": "textured layered wolf cut shaggy messy hairstyle",
        }
        return prompts.get(style_id, "hair style transformation")

    def _generate_with_pillow(self, img_path_or_base64: str, style_id: str, color: str) -> bytes:
        """Процедурная генерация через Pillow (fallback)."""
        try:
            image_data = self._load_image(img_path_or_base64)
        except Exception as e:
            raise ValueError(f"Cannot load image: {e}")

        w, h = image_data.size
        target_r, target_g, target_b = HAIR_COLORS.get(color or "ash_gray", HAIR_COLORS["ash_gray"])

        result = self._apply_hair_color(image_data, target_r, target_g, target_b, w, h)

        if style_id == "bob":
            result = self._apply_bob_cut(result, w, h)
        elif style_id == "cascade":
            result = self._apply_cascade(result, w, h)
        elif style_id == "pixie":
            result = self._apply_pixie(result, w, h)
        elif style_id == "wolfcut":
            result = self._apply_wolfcut(result, w, h)
        elif style_id == "hollywood":
            result = self._apply_hollywood(result, w, h)
        elif style_id == "high_bun":
            result = self._apply_high_bun(result, w, h)
        elif style_id == "low_bun":
            result = self._apply_low_bun(result, w, h)
        elif style_id == "greek_braid":
            result = self._apply_greek_braid(result, w, h)
        elif style_id == "french_twist":
            result = self._apply_french_twist(result, w, h)
        elif style_id == "blowout":
            result = self._apply_blowout(result, w, h)
        elif style_id == "beach_waves":
            result = self._apply_beach_waves(result, w, h)
        elif style_id == "wet_hair":
            result = self._apply_wet_hair(result, w, h)
        elif style_id == "high_ponytail":
            result = self._apply_high_ponytail(result, w, h)
        elif style_id == "straight_hair":
            result = self._apply_straightening(result, w, h)

        buffer = BytesIO()
        result.save(buffer, format="PNG")
        return buffer.getvalue()

    def _load_image(self, img_path_or_base64: str):
        """Загружает изображение из пути или base64."""
        if isinstance(img_path_or_base64, bytes) or img_path_or_base64.startswith("data:image"):
            image_data = Image.open(io.BytesIO(base64.b64decode(img_path_or_base64.split(",", 1)[1] if "," in img_path_or_base64 else img_path_or_base64))).convert("RGB").copy()
        else:
            try:
                image_data = Image.open(img_path_or_base64).convert("RGB").copy()
            except Exception as e:
                raise ValueError(f"Cannot load image: {e}")

        return image_data

    def _apply_hair_color(self, img, r, g, b, w, h):
        """Применяет пепельный цвет волос."""
        result = img.copy()
        for y in range(h):
            row_r, row_g, row_b = result.getpixel((0, y)), result.getpixel((w//2-1, y)), result.getpixel((w-1, y))
            pixel_row = np.array([row_r[0], row_g[1], row_b[2]])
            if np.std(pixel_row) > 25 and np.mean(pixel_row) > 80:
                new_r = int(row_r[0] * 0.6 + r * 0.4)
                new_g = int(row_g[1] * 0.6 + g * 0.4)
                new_b = int(row_b[2] * 0.6 + b * 0.4)
                noise = np.random.randint(-3, 4, size=3)
                result.putpixel((w//2 + random.randint(5, w - w//4), y), (
                    max(0, min(255, new_r + noise[0])),
                    max(0, min(255, new_g + noise[1])),
                    max(0, min(255, new_b + noise[2]))
                ))
        return result

    def _apply_bob_cut(self, img, w, h):
        """Применяет стрижку боб."""
        result = img.copy()
        hair_top = max(75, h * 0.68)
        for y in range(hair_top):
            if random.random() > 0.3:
                x_idx = random.randint(0, w - 1)
                left_boundary = min(int(hair_top - y * 0.7), h - 1)
                right_boundary = min(int(hair_top + random.randint(-5, 8)), h - 1)
                if x_idx < w * 0.4:
                    if random.random() > 0.2 or y < left_boundary:
                        result.putpixel((x_idx, y), (168, 169, 173))
                else:
                    if random.random() > 0.4 or y < right_boundary:
                        result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_cascade(self, img, w, h):
        """Применяет каскад."""
        result = img.copy()
        hair_top = max(90, h * 0.72)
        for y in range(hair_top):
            if random.random() > 0.25:
                x_idx = random.randint(0, w - 1)
                level = min(hair_top + random.randint(-10, 15), h - 1)
                if y <= level:
                    result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_pixie(self, img, w, h):
        """Применяет пикси."""
        result = img.copy()
        hair_top = max(45, h * 0.38)
        for y in range(hair_top):
            if random.random() > 0.15:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_wolfcut(self, img, w, h):
        """Применяет волфкат."""
        result = img.copy()
        hair_top = max(95, h * 0.74)
        for y in range(hair_top):
            if y < 35 and random.random() > 0.1:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
            elif y < hair_top - 20 and random.random() > 0.35:
                x_idx = random.randint(int(w * 0.2), int(w * 0.7))
                result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_hollywood(self, img, w, h):
        """Применяет голливудские волны."""
        result = img.copy()
        hair_top = max(105, h * 0.78)
        for y in range(hair_top):
            if random.random() > 0.2:
                x_idx = random.randint(int(w * 0.3), w - 1)
                wave_height = min(4 + (y % 12), h // 6)
                result.putpixel((x_idx, y), (168, 169, 173))

        # Добавить крупную волну на одну сторону
        for y in range(hair_top):
            wave_offset = int(w * 0.5 + random.randint(-2, 2))
            result.putpixel((wave_offset, y), (168, 169, 173))

        return result

    def _apply_high_bun(self, img, w, h):
        """Применяет высокий пучок."""
        result = img.copy()
        hair_top = max(95, h * 0.7)
        for y in range(hair_top):
            if random.random() > 0.2:
                x_idx = random.randint(int(w * 0.3), int(w * 0.6))
                result.putpixel((x_idx, y), (168, 169, 173))

        # Объем у корней
        for y in range(45, hair_top - 25):
            x_idx = random.randint(int(w * 0.2), int(w * 0.8))
            result.putpixel((x_idx, y), (168, 169, 173))

        return result

    def _apply_low_bun(self, img, w, h):
        """Применяет низкий пучок."""
        result = img.copy()
        hair_top = max(85, h * 0.25)
        for y in range(hair_top):
            if random.random() > 0.2:
                x_idx = random.randint(int(w * 0.3), int(w * 0.6))
                result.putpixel((x_idx, y), (168, 169, 173))

        return result

    def _apply_greek_braid(self, img, w, h):
        """Применяет греческую косу."""
        result = img.copy()
        hair_top = max(105, h * 0.8)
        for y in range(hair_top):
            if random.random() > 0.2:
                # Пышная коса по центру
                x_idx = int(w / 2) + random.randint(-3, 3)
                result.putpixel((x_idx, y), (168, 169, 173))

        return result

    def _apply_french_twist(self, img, w, h):
        """Применяет французский твист."""
        result = img.copy()
        hair_top = max(100, h * 0.75)
        for y in range(hair_top):
            if random.random() > 0.2:
                x_idx = random.randint(int(w * 0.3), int(w * 0.6))
                result.putpixel((x_idx, y), (168, 169, 173))

        return result

    def _apply_blowout(self, img, w, h):
        """Применяет брашинг-объем."""
        result = img.copy()
        hair_top = max(95, h * 0.8)
        for y in range(hair_top):
            if random.random() > 0.2:
                x_idx = random.randint(int(w * 0.3), int(w * 0.7))
                result.putpixel((x_idx, y), (168, 169, 173))

        # Объем у корней
        for y in range(45, hair_top - 20):
            x_idx = random.randint(int(w * 0.2), int(w * 0.8))
            result.putpixel((x_idx, y), (168, 169, 173))

        return result

    def _apply_beach_waves(self, img, w, h):
        """Применяет пляжные волны."""
        result = img.copy()
        hair_top = max(105, h * 0.82)
        for y in range(hair_top):
            if random.random() > 0.3:
                wave_width = random.randint(6, 14)
                x_start = random.randint(int(w * 0.2), int(w * 0.5))
                for dx in range(-wave_width // 2, wave_width // 2):
                    if x_start + dx >= 0 and x_start + dx < w:
                        result.putpixel((x_start + dx, y), (168, 169, 173))

        return result

    def _apply_wet_hair(self, img, w, h):
        """Применяет эффект влажных волос."""
        result = img.copy()
        hair_top = max(105, h * 0.8)
        for y in range(hair_top):
            if random.random() > 0.25:
                x_idx = random.randint(int(w * 0.2), int(w * 0.7))
                result.putpixel((x_idx, y), (168, 169, 173))

        # Добавить эффект геля (блестки)
        for _ in range(5):
            x = random.randint(int(w * 0.2), int(w * 0.7))
            y = random.randint(int(hair_top - 30), hair_top)
            result.putpixel((x, y), (168, 169, 173))

        return result

    def _apply_high_ponytail(self, img, w, h):
        """Применяет высокий текстурный хвост."""
        result = img.copy()
        hair_top = max(105, h * 0.82)
        for y in range(hair_top):
            if random.random() > 0.2:
                x_idx = random.randint(int(w * 0.3), int(w * 0.7))
                result.putpixel((x_idx, y), (168, 169, 173))

        # Начес у корней
        for y in range(45, hair_top - 25):
            x_idx = random.randint(int(w * 0.2), int(w * 0.8))
            result.putpixel((x_idx, y), (168, 169, 173))

        return result

    def _apply_straightening(self, img, w, h):
        """Применяет идеально прямые волосы."""
        result = img.copy()
        hair_top = max(105, h * 0.8)
        for y in range(hair_top):
            if random.random() > 0.1:
                x_idx = random.randint(int(w * 0.2), int(w * 0.7))
                result.putpixel((x_idx, y), (168, 169, 173))

        return result

    def _apply_strand_detail(self, img, w, h):
        """Добавляет детали прядей."""
        result = img.copy()
        for _ in range(8):
            strand_w = random.randint(4, 12)
            strand_h = random.randint(h // 3, int(h * 0.7))
            x_start = random.randint(int(w * 0.1), int(w * 0.5))
            y_start = random.randint(hair_top - strand_h, hair_top)
            for dy in range(strand_h):
                if x_start + dy < w:
                    result.putpixel((x_start + dy, y_start + dy // 3), (168, 169, 173))

        return result


generator = HairStyleGenerator()


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Beauty Haircut API", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Проверка здоровья API."""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post("/api/generate")
async def generate_haircut(image_url: str, style_id: str, color: Optional[str] = None) -> dict:
    """Генерирует изображение с заданным стилем прически и цветом волос."""
    logger.info(f"[API] Request received: image={image_url[:50]}..., style={style_id}, color={color}")

    try:
        bytes_data = generator.generate(image_url, style_id, color or "ash_gray")

        result_path = OUTPUT_DIR / f"{style_id}_{color or 'ash_gray'}_{int(datetime.now(timezone.utc).timestamp()) * 1000}.png"
        with open(result_path, "wb") as f:
            f.write(bytes_data)

        logger.info(f"[API] saved to {result_path} ({len(bytes_data)} bytes)")

        return {
            "success": True,
            "style_id": style_id,
            "color": color or "ash_gray",
            "result_url": f"/api/download/{result_path.name}",
            "metadata": {"generated_at": datetime.now(timezone.utc).isoformat(), "hash": result_path.stem},
        }

    except Exception as e:
        logger.error(f"[API] Generation failed for {image_url}: {e!r}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{filename}")
async def download_result(filename: str):
    """Скачивает сгенерированное изображение."""
    path = OUTPUT_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    from fastapi.responses import FileResponse
    return FileResponse(str(path))


@app.get("/api/styles")
async def list_styles():
    """Возвращает список всех доступных стилей причесок."""
    return {"styles": list(HAIRSTYLES.values()), "total": len(HAIRSTYLES)}


# --- Qwen Image 2.1 — инструкция по установке ---
# После скачивания модели в ./models/qwen-image-v1.5 установите:
#   pip install transformers torch torchvision
# Затем в backend.py измените QWEN_ENABLE = True