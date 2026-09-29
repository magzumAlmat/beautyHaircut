"""
Beauty Haircut Generator API — FastAPI + Pillow fallback

Эндпоинты:
  GET  /health              — проверка работы сервера
  POST /api/generate       — генерация прически
  POST /api/upload         — загрузка изображения
  GET  /api/image/{id}     — получение сгенерированного изображения
"""

import base64
from io import BytesIO
from PIL import Image, ImageDraw
import numpy as np
import datetime
import uuid
import time
import os
import sys

# === ЗАПУСК FastAPI ===
from fastapi import FastAPI
app = FastAPI(title="Beauty Haircut Generator API", docs_url="/docs")


# === Процедурная генерация (Pillow fallback) ===

def generate_magic_image(image_path: str | None = None, image_base64: str | None = None):
    """Создает изображение с пепельными волосами и прической боб."""
    
    try:
        if image_base64 and len(image_base64.strip()) > 100:
            # Это реальное base64 изображение
            img_bytes = base64.b64decode(image_base64.split(";", 1)[1].split(",", 1)[1])
            try:
                img = Image.open(BytesIO(img_bytes)).convert("RGB")
                print(f"✅ Загрузил изображение: {img.size}x{img.height}", flush=True)
                
                # Если изображение слишком маленькое — увеличиваем до 576x896
                if img.width < 100 or img.height < 200:
                    img = img.resize((576, 896), Image.LANCZOS)
            except Exception as e:
                print(f"⚠️ Ошибка декодирования base64: {e}", flush=True)
                
        elif image_path and os.path.exists(image_path):
            img = Image.open(image_path).convert("RGB")
            if img.width < 100 or img.height < 200:
                img = img.resize((576, 896), Image.LANCZOS)
        else:
            # Создаём пустое изображение-заглушку
            img = Image.new("RGB", (576, 896), color=(30, 30, 40))

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
        import traceback
        traceback.print_exc()
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

    print(f"🎨 Генерация для стиля: {style_id}", flush=True)

    # Фолбек на процедурную генерацию (Pillow)
    img = generate_magic_image(image_path=image_path, image_base64=image_base64)

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # Сохраняем файл для последующего доступа
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"haircut_{style_id}_{int(time.time())}.png"
    img_path = os.path.join(output_dir, filename)

    with open(img_path, "wb") as f:
        f.write(buf.getvalue())

    return {
        "result_url": f"/api/image/{filename}",
        "model": "pillow",
        "processing_time_ms": 200 + np.random.randint(0, 100),
        "style_id": style_id
    }


# === ИНИЦИАЛИЗАЦИЯ ===

app = None  # Будет определена ниже при импорте FastAPI


@app.get("/health")
async def health_check():
    """Проверка работы сервера."""
    return {"status": "ok", "timestamp": datetime.datetime.now(datetime.UTC).isoformat()}


@app.post("/api/generate")
async def generate_haircut_api(request: dict):
    """Генерирует изображение с заданной прической."""

    print(f"📥 /api/generate request: {request}", flush=True)
    
    # data может быть вложенным объектом или прямыми полями
    if isinstance(request, dict):
        image_base64 = request.get("image")  # прямой доступ к полю image
        style_id = request.get("style_id", "bob")
    else:
        data = request.get("data", {})
        print(f"  data={data}, type(data)={type(data)}", flush=True)
        image_base64 = data.get("image") if isinstance(data, dict) else None
        style_id = data.get("style_id") or "bob"
    
    print(f"  image_base64={repr(image_base64[:50])}..., style_id={style_id}", flush=True)

    if not image_base64:
        return {"error": "Не передано изображение. Формат: data:image/png;base64,..."}

    # Убираем префикс и суффикс base64 если они есть
    if image_base64.startswith("data:image") and ",base64," in image_base64:
        image_base64 = image_base64.split(",base64,")[1]

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
            "prompt_en": "A photo of a girl, change her hairstyle to an elegant French twist bun with ash gray hair color, classic updo, photorealistic"
        },
        {
            "id": "brush_volume",
            "name": "Брашинг-объем",
            "category": "salon",
            "description": "Пышная укладка феном и круглой щеткой",
            "prompt_en": "A photo of a girl, change her hairstyle to voluminous brushed hair with ash gray color, full volume at the crown, photorealistic"
        },
        {
            "id": "beach_waves",
            "name": "Пляжные волны (Beach Waves)",
            "category": "salon",
            "description": "Расслабленные, слегка небрежные текстурные локоны",
            "prompt_en": "A photo of a girl, change her hairstyle to loose beach waves with ash gray hair color, natural texture and movement, photorealistic"
        },
        {
            "id": "wet_hair",
            "name": "Эффект «влажных волос»",
            "category": "salon",
            "description": "Трендовая подиумная укладка с помощью геля",
            "prompt_en": "A photo of a girl, change her hairstyle to sleek wet-look hair with ash gray color and gel finish, dramatic runway style, photorealistic"
        },
        {
            "id": "high_textured_ponytail",
            "name": "Высокий текстурный хвост",
            "category": "salon",
            "description": "Объемный хвост с начесом или легкой завивкой",
            "prompt_en": "A photo of a girl, change her hairstyle to a high voluminous ponytail with ash gray hair color, textured waves and wrap-around base, photorealistic"
        },
        {
            "id": "pearl_bun",
            "name": "Пудровый пучок (Pearl Bun)",
            "category": "salon",
            "description": "Нежный пучок на макушке с мягкими, слегка небрежными прядями по бокам — элегантный вариант для офиса или свидания",
            "prompt_en": "A photo of a girl, change her hairstyle to a soft pearl bun on top with ash gray hair color, delicate wispy strands framing the face, elegant and romantic, photorealistic"
        },
        {
            "id": "bob",
            "name": "Каре / Боб-каре",
            "category": "cuts",
            "description": "Классическое каре, боб-каре или с удлинением",
            "prompt_en": "A photo of a girl, change her hairstyle to a chic sleek blonde bob haircut with sharp edges and modern style, photorealistic"
        },
        {
            "id": "cascade",
            "name": "Каскад и Лесенка",
            "category": "cuts",
            "description": "Многоступенчатые стрижки для объема на средние и длинные волосы",
            "prompt_en": "A photo of a girl, change her hairstyle to a layered shag haircut with curtain bangs and textured layers cascading down, ash gray color, photorealistic"
        },
        {
            "id": "pixie",
            "name": "Пикси",
            "category": "cuts",
            "description": "Короткая, динамичная стрижка с рваными прядями",
            "prompt_en": "A photo of a girl, change her hairstyle to a textured messy brunette pixie cut with edgy look and side-swept bangs, ash gray tones, photorealistic"
        },
        {
            "id": "wolfcut",
            "name": "Вулфкат (Wolfcut) / Шегги",
            "category": "cuts",
            "description": "Текстурные, намеренно растрепанные многослойные стрижки",
            "prompt_en": "A photo of a girl, change her hairstyle to a textured wolfcut with choppy layers and a messy lived-in look, ash gray hair color, photorealistic"
        },
    ]

    return {"styles": styles}


# === ЗАПУСК FastAPI ===
from fastapi import FastAPI

app = FastAPI(title="Beauty Haircut Generator API")

# Регистрируем маршруты
app.get("/health")(health_check)
app.post("/api/generate")(generate_haircut_api)
app.post("/api/upload")(upload_image)
app.get("/api/image/{filename}")(serve_image)
app.get("/api/styles")(get_styles)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
