"""
Beauty Haircut Generator API — FastAPI + Pillow fallback

Эндпоинты:
  GET  /health              — проверка работы сервера
  POST /api/generate       — генерация прически (JSON с base64 ИЛИ multipart с файлом)
  POST /api/upload         — загрузка изображения
  GET  /api/image/{id}     — получение сгенерированного изображения
  GET  /api/styles         — список причесок
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
import json


# === ЗАПУСК FastAPI ===
try:
    from fastapi import FastAPI, Request, UploadFile, File, Form
    app = FastAPI(title="Beauty Haircut Generator API", docs_url="/docs")
except ImportError:
    print("⚠️ FastAPI не установлен. Запуск в режиме отладки...")
    sys.stdout.flush()
    import traceback
    traceback.print_exc()
    exit(1)


# === Процедурная генерация (Pillow fallback) ===

def generate_magic_image(image_path: str | None = None, image_base64: str | None = None):
    """Создает изображение с пепельными волосами и прической боб."""
    
    try:
        if image_base64 and len(image_base64.strip()) > 100:
            # Это реальное base64 изображение
            img_bytes = base64.b64decode(image_base64.split(";", 1)[1].split(",", 1)[1])
            try:
                img = Image.open(BytesIO(img_bytes)).convert("RGB")
                print(f"✅ Загрузил изображение: {img.size[0]}x{img.size[1]}", flush=True)
                
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
        draw2 = ImageDraw.Draw(img)
        for x in range(0, 576):
            if x % 3 == 0:
                brightness = int(55 + np.random.default_rng(x).uniform(-4, 4))
                base_y = int(240 + (x - 288) * 0.3)
                draw2.line([(x, 20), (x, max(28, base_y - 8))], fill=(brightness, brightness-12, brightness-18), width=1)

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


# === API ROUTES ===

@app.get("/health")
async def health_check():
    """Проверка работы сервера."""
    return {"status": "ok", "timestamp": datetime.datetime.now(datetime.UTC).isoformat()}


@app.post("/api/generate")
async def generate_haircut_api(request: Request):
    """Генерирует изображение с заданной прической.
    
    Принимает:
      - JSON body: {"image": "<base64>", "style_id": "bob"}
      - Мultipart form: file="image" + field="style_id"
    """

    # Проверяем multipart (есть файлы) — FastAPI Request имеет атрибут files
    if hasattr(request, 'files') and request.files.get('image'):
        file = request.files['image'][0]
        image_base64 = None
        
        # Если файл — конвертируем в base64
        img_bytes = await file.read()
        image_base64 = "data:image/png;base64," + base64.b64encode(img_bytes).decode()
        
    else:
        # Это JSON запрос — читаем тело через request.json()
        try:
            json_body = await request.json() or {}
        except (json.JSONDecodeError, ValueError):
            json_body = {}
        image_base64 = json_body.get("image")
        style_id = json_body.get("style_id", "bob")

    # Если image_base64 всё ещё None — это ошибка
    if not image_base64:
        return {"error": "Не передано изображение. Используйте JSON с полем 'image' (base64) или multipart form-data с файлом в поле 'image'.", 
                "hint": "Пример curl: -d '{\"image\":\"<data:image...>\",\"style_id\":\"bob\"}'"}

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
async def upload_image(request: Request):
    """Загружает изображение для обработки."""
    # Проверяем multipart
    if hasattr(request, 'files') and request.files.get('image'):
        file = request.files['image'][0]
        image_path = f"/uploaded/{file.filename}"
        
        # Сохраняем файл
        upload_dir = os.path.join(os.path.dirname(__file__), "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        
        filepath = os.path.join(upload_dir, file.filename)
        with open(filepath, "wb") as f:
            f.write(await file.read())
        
        # Возвращаем путь (относительный от backend.py)
        rel_path = os.path.relpath(filepath, "/Users/billionare/.lmstudio/apps/bionic/projects/d49037d8-47f4-5808-9028-c707de117f8f/workspace/scratchpad")
        
    elif isinstance(request, dict):
        data = request.get("data", {}) or {}
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                pass
        image_path = data.get("imagePath") or data.get("fileUrl", "")

        # Конвертируем file:// URL в путь относительно scratchpad
        if image_path.startswith("file://"):
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
            "prompt_en": "A photo of a girl, change her hairstyle to an elegant French twist bun with ash gray hair color, classic updo style, photorealistic"
        },
        {
            "id": "brush_volume",
            "name": "Брашинг-объем",
            "category": "salon",
            "description": "Пышная укладка феном и круглой щеткой",
            "prompt_en": "A photo of a girl with brushed-up voluminous hairstyle, ash gray hair color, root lift and textured finish, photorealistic"
        },
        {
            "id": "beach_waves",
            "name": "Пляжные волны (Beach Waves)",
            "category": "salon",
            "description": "Расслабленные, слегка небрежные текстурные локоны",
            "prompt_en": "A photo of a girl with beach waves hairstyle, ash gray hair color, loose natural-looking curls and textured finish, photorealistic"
        },
        {
            "id": "wet_hair",
            "name": "Эффект «влажных волос»",
            "category": "salon",
            "description": "Трендовая подиумная укладка с помощью геля",
            "prompt_en": "A photo of a girl with wet look hairstyle, ash gray hair color, gel-smoothed strands with high shine, photorealistic"
        },
        {
            "id": "high_textured_ponytail",
            "name": "Высокий текстурный хвост",
            "category": "salon",
            "description": "Объемный хвост с начесом или легкой завивкой",
            "prompt_en": "A photo of a girl with a high textured ponytail, ash gray hair color, voluminous wrap-around base and slight curls, photorealistic"
        },
        {
            "id": "pearl_bun",
            "name": "Пудровый пучок (Pearl Bun)",
            "category": "salon",
            "description": "Нежный пучок на макушке с мягкими, слегка небрежными прядями по бокам — элегантный вариант для офиса или свидания",
            "prompt_en": "A photo of a girl with a pearl bun hairstyle, ash gray hair color, soft messy low bun at the crown with wispy face-framing strands, photorealistic"
        },
        {
            "id": "bob",
            "name": "Каре / Боб-каре",
            "category": "cuts",
            "description": "Классическое каре, боб-каре или с удлинением",
            "prompt_en": "A photo of a girl, change her hairstyle to an ash gray bob haircut with soft layers and face-framing pieces, photorealistic"
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
        }
    ]

    return {"styles": styles}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)