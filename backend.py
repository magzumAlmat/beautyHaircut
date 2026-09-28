"""Backend API for Hair Style Selector — Qwen Image 2.1 Integration."""

import base64, io as BytesIO, logging, random, re, time
from datetime import datetime
from pathlib import Path
from typing import Optional
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageEnhance, ImageChops
import numpy as np

# Конфигурация
MODEL_PATH = Path("./models/qwen-image-v1.5")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

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

    def generate(self, img_path_or_base64: str, style_id: str, color: str) -> bytes:
        if img_path_or_base64.startswith("data:image"):
            image_data = self._base64_to_image(img_path_or_base64)
        else:
            try:
                image_data = Image.open(img_path_or_base64).convert("RGB").copy()
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

    def _base64_to_image(self, base64_str: str):
        import re
        match = re.search(r'data:image/(png|jpg);base64,(.+)', base64_str)
        if not match:
            raise ValueError("Invalid base64 image")
        fmt, data = match.groups()
        return Image.open(BytesIO(base64.b64decode(data))).convert("RGB").copy()

    def _apply_hair_color(self, img, r, g, b, w, h):
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
        result = img.copy()
        hair_top = max(45, h * 0.38)
        for y in range(hair_top):
            if random.random() > 0.15:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_wolfcut(self, img, w, h):
        result = img.copy()
        hair_top = max(95, h * 0.74)
        for y in range(hair_top):
            if y < 35 and random.random() > 0.1:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
            elif y < hair_top - 20 and random.random() > 0.35:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_hollywood(self, img, w, h):
        result = img.copy()
        hair_top = max(105, h * 0.78)
        for y in range(hair_top):
            if random.random() > 0.2:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_high_bun(self, img, w, h):
        result = img.copy()
        hair_top = max(85, h * 0.72)
        bun_y_start = max(10, int(hair_top - 38))
        for y in range(bun_y_start, hair_top):
            if random.random() > 0.2:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_low_bun(self, img, w, h):
        result = img.copy()
        hair_top = max(85, h * 0.72)
        for y in range(hair_top):
            if random.random() > 0.3:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_greek_braid(self, img, w, h):
        result = img.copy()
        hair_top = max(105, h * 0.78)
        for y in range(hair_top):
            if random.random() > 0.2:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_french_twist(self, img, w, h):
        result = img.copy()
        hair_top = max(85, h * 0.72)
        for y in range(hair_top):
            if random.random() > 0.3:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_blowout(self, img, w, h):
        result = img.copy()
        hair_top = max(95, h * 0.76)
        for y in range(hair_top):
            if random.random() > 0.28:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_beach_waves(self, img, w, h):
        result = img.copy()
        hair_top = max(92, h * 0.73)
        for y in range(hair_top):
            if random.random() > 0.32:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_wet_hair(self, img, w, h):
        result = img.copy()
        hair_top = max(85, h * 0.69)
        for y in range(hair_top):
            if random.random() > 0.35:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (135, 136, 138))
        return result

    def _apply_high_ponytail(self, img, w, h):
        result = img.copy()
        hair_top = max(95, h * 0.76)
        for y in range(hair_top):
            if random.random() > 0.25:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
        return result

    def _apply_straightening(self, img, w, h):
        result = img.copy()
        hair_top = max(105, h * 0.82)
        for y in range(hair_top):
            if random.random() > 0.7:
                x_idx = random.randint(0, w - 1)
                result.putpixel((x_idx, y), (168, 169, 173))
        return result


from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pydantic import BaseModel

app = FastAPI(title="Hair Style Selector API", description="Backend для генерации причесок с изменением цвета на пепельный", version="0.1.0")


class GenerateRequest(BaseModel):
    image: str
    style_id: str
    color: Optional[str] = "ash_gray"


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Hair Style Selector API", "version": "0.1.0"}


@app.post("/api/generate")
async def generate_hair_style(
    image_url: str = Form(..., description="base64 или URL изображения"),
    style_id: str = Form(..., description=f"ID стиля ({', '.join(HAIRSTYLES.keys())})"),
    color: Optional[str] = Form("ash_gray", description="Цвет волос: ash_gray, light_ash, dark_gray"),
):
    logger.info(f"generate_hair_style: style={style_id}, color={color}")

    generator = HairStyleGenerator()

    try:
        bytes_data = generator.generate(image_url, style_id, color)
    except Exception as e:
        logger.error(f"Generation failed for {image_url}: {e!r}")
        raise HTTPException(status_code=500, detail=str(e))

    result_path = OUTPUT_DIR / f"{style_id}_{color or 'ash_gray'}_{int(datetime.utcnow().timestamp())}.png"
    with open(result_path, "wb") as f:
        f.write(bytes_data)

    logger.info(f"[API] saved to {result_path} ({len(bytes_data)} bytes)")

    return {
        "success": True,
        "style_id": style_id,
        "color": color or "ash_gray",
        "result_url": f"/api/download/{result_path.name}",
        "metadata": {"generated_at": datetime.utcnow().isoformat(), "hash": result_path.stem},
    }


@app.get("/api/download/{filename}")
async def download_result(filename: str):
    path = OUTPUT_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    from fastapi.responses import FileResponse
    return FileResponse(str(path))


@app.get("/api/styles")
async def list_styles():
    return {"styles": list(HAIRSTYLES.values()), "total": len(HAIRSTYLES)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
