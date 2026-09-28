"""
Backend API for Hair Style Selector — Qwen Image 2.1 Integration

Служит мостом между React-frontend и моделью Qwen Image 2.1 для генерации:
- Изменения цвета волос (пепельный / ash gray)
- Стрижки боб (bob haircut)
- И других причесок из списка UI

Запуск: uvicorn backend:app --reload --host 0.0.0.0 --port 8001
"""

import base64
from pathlib import Path
from typing import Optional, Literal
from enum import Enum
from datetime import datetime

# --- Импорт PyTorch и модели (если доступна) ---
try:
    import torch
    from PIL import Image
    import numpy as np
except ImportError:
    # Fallback режим без GPU — эмуляция через Pillow + цветовая коррекция
    has_torch = False
else:
    has_torch = True


# ==================== Конфигурация ====================

MODEL_PATH = Path("./models/qwen-image-v1.5")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Цвета волос (палитра для пепельного и других оттенков)
HAIR_COLORS: dict[str, tuple[int, int, int]] = {
    "ash_gray":       (168, 169, 173),   # #A8A9AD — классический пепельный
    "light_ash":      (192, 192, 200),   # #C0C0C8 — светло-пепельный
    "dark_gray":      (112, 112, 112),   # #707070 — тёмно-серый
    "platinum":       (225, 230, 235),   # #E1E6EB — платиновый блонд
    "ebony_gray":     (90, 92, 94),      # #5A5C5E — угольно-серый
}

# Стрижки боб с параметрами геометрии
BOB_STYLES: dict[str, dict] = {
    "bob_center": {
        "name": "Каре (center part)",
        "parting": "center",
        "length_mm": 95,
        "layers": [(-45, 20), (0, 16), (45, 12)],
    },
    "bob_side_left": {
        "name": "Боб асимметричный (влево)",
        "parting": "side_left",
        "length_mm": 85,
        "layers": [(-30, 24), (-10, 18), (30, 12)],
    },
    "bob_side_right": {
        "name": "Боб асимметричный (вправо)",
        "parting": "side_right",
        "length_mm": 90,
        "layers": [(45, 22), (10, 16), (-30, 12)],
    },
}

# Логи для трассировки
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==================== Модель Qwen Image 2.1 ====================

class StyleType(Enum):
    """Типы модификаций (для API)."""
    COLOR_CHANGE = "color_change"      # Изменение цвета волос
    BOB_CUT = "bob_cut"                # Стрижка боб
    HAIR_COLOR = "hair_color"          # Изменение оттенка


class QwenImageModel:
    """Класс-обёртка для модели Qwen Image 2.1 (или её эмуляция без GPU)."""

    def __init__(self, path: Path):
        self.model_path = path
        has_torch = "torch" in globals() or False
        self.has_gpu = torch.cuda.is_available() if has_torch else False
        logger.info(
            f"[QwenImageModel] model_path={path}, "
            f"has_torch={has_torch}, "
            f"cuda_available={self.has_gpu}"
        )

    def _encode_image(self, image: Image.Image) -> str:
        """Кодирование изображения в base64 (для сохранения результата)."""
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def generate_hair_color(self, image: Image.Image) -> tuple[Image.Image, dict]:
        """
        Генерация изображения с изменением цвета волос на пепельный.

        Реализует процедурную цветовую коррекцию + маска области волос.

        Args:
            image: PIL Image (RGB).

        Returns:
            Tuple[PIL.Image, dict] — обработанное изображение и метаданные.
        """
        # --- В режиме с PyTorch можно было бы использовать модель Qwen2.5-VL ---
        # Здесь эмуляция через Pillow + цветовую коррекцию по зонам.

        img = image.convert("RGB").copy()
        w, h = img.size

        # Простая маска волос (примерная — на практике нужно обучать детектор)
        # Оцениваем яркость и насыщенность для выделения волос
        mask = np.zeros((h, w), dtype=np.uint8)

        for y in range(h):
            row = img.getpixel((0, y))
            avg_r, avg_g, avg_b = (row[0] + row[w // 2 - 1][1] + row[w - 1][2]) / 3
            # Волосы обычно темные и насыщенного цвета — выделяем по контрасту
            if np.std(img.getchannel("R")[:, y][:, None]) > 20:
                mask[y] = min(255, int(np.mean(mask[y])))

        # Применяем пепельный цвет волос
        target_color = HAIR_COLORS["ash_gray"]

        for y in range(h):
            row_r, row_g, row_b = img.load()[y]
            # Простая линейная интерполяция: 70% оригинал + 30% целевой цвет
            new_r = int(row_r * 0.7 + target_color[0] * 0.3)
            new_g = int(row_g * 0.7 + target_color[1] * 0.3)
            new_b = int(row_b * 0.7 + target_color[2] * 0.3)

            # Добавляем шум для текстуры
            noise_r, noise_g, noise_b = np.random.randint(-8, 9, size=3)
            img.putpixel((w // 4 + np.random.randint(10, w - w//4), y), (
                max(0, min(255, new_r + noise_r)),
                max(0, min(255, new_g + noise_g)),
                max(0, min(255, new_b + noise_b))
            ))

        logger.info(f"[QwenImageModel] color change: target={target_color}")
        return img, {"color": "ash_gray", "mode": "procedural"}


class FallbackGenerator:
    """FALLBACK генератор при отсутствии модели — процедурная эмуляция."""

    def apply_style(self, image_path: str, style_id: str) -> tuple[str, dict]:
        from PIL import Image, ImageFilter, ImageEnhance

        img = Image.open(image_path).convert("RGB")
        w, h = img.size

        result = img.copy()
        metadata = {
            "style": style_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

        # --- Эмуляция прически через цветовую коррекцию и фильтры ---
        if style_id in ("bob", "pixie", "wolfcut"):
            result = self._apply_bob_cut(result)
        elif style_id == "hollywood":
            result = self._apply_hollywood_waves(result)
        elif style_id == "straight_hair":
            result = self._apply_straightening(result)

        metadata["mode"] = "fallback_procedural"
        logger.info(f"[FallbackGenerator] applied style={style_id} to {image_path}")

        buffer = BytesIO()
        result.save(buffer, format="PNG")
        return buffer.getvalue(), metadata


# ==================== API (FastAPI) ====================

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pydantic import BaseModel
import io as BytesIO

app = FastAPI(
    title="Hair Style Selector API",
    description="Backend для генерации причесок с Qwen Image 2.1 (или fallback)",
    version="0.1.0",
)


# Pydantic схемы
class GenerateRequest(BaseModel):
    image: str                              # URL или base64
    style_id: str                           # bob | pixie | wolfcut | hollywood ...
    color: Optional[str] = "ash_gray"       # ash_gray, light_ash, dark_gray


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok", "service": "Hair Style Selector API"}


@app.post("/api/generate")
async def generate_hair_style(
    image_url: str = Form(...),
    style_id: str = Form(...),
    color: Optional[str] = Form("ash_gray"),
):
    """
    Генерация изображения с применённой прической.

    **style_id** — один из 24 вариантов (см. список в UI).
    **color** — цвет волос: `ash_gray`, `light_ash`, `dark_gray`.
    """
    logger.info(f"generate_hair_style called with image_url={image_url[:60]}..., style_id={style_id}, color={color}")

    # Фолбэк-генерация (можно заменить на реальный вызов модели Qwen Image 2.1)
    generator = FallbackGenerator()
    bytes_data, meta = generator.apply_style(image_url, style_id)

    result_path = OUTPUT_DIR / f"{style_id}_{color}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.png"

    with open(result_path, "wb") as f:
        f.write(bytes_data)

    logger.info(f"[API] saved result to {result_path} ({len(bytes_data)} bytes)")

    return {
        "success": True,
        "style_id": style_id,
        "color": color or "ash_gray",
        "result_url": f"/api/download/{result_path.name}",
        "metadata": meta,
    }


@app.get("/api/download/{filename}")
async def download_result(filename: str):
    path = OUTPUT_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    from fastapi.responses import FileResponse
    return FileResponse(str(path))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
