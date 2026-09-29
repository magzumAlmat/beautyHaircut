# 🤖 Qwen Image 2.1 — установка и запуск

## ⚡ Быстрый старт

### Способ 1: Установка через скрипт (рекомендуется)

```bash
cd /scratchpad
./scripts/setup_qwen.sh
```

Это установит все зависимости и скачает модель (~6 ГБ).

---

### Способ 2: Ручная установка

```bash
# Шаг 1: Установить зависимости
pip install transformers torch torchvision pillow requests huggingface_hub accelerate bitsandbytes xformers

# Шаг 2: Скачать модель (около 6 GB)
huggingface-cli download Qwen/Qwen2.5-Image-VL-Instruct \
    --local-dir ./models/qwen-image-v1.5 --repo-type model --force-download

# Шаг 3: Запустить сервер
cd /scratchpad && python backend_qwen.py
```

---

## 📋 Что делает этот скрипт?

`backend_qwen.py` — это отдельный HTTP-сервер, который:

1. Принимает POST запрос на `/generate`
2. Загружает изображение (URL или base64)
3. Генерирует новое изображение через Qwen Image 2.1
4. Возвращает PNG файл

---

## 🔄 Интеграция с существующим backend.py

Вместо того чтобы менять `backend.py`, запускаем **отдельный** сервер на порту **8080**:

```bash
# В одной вкладке — старый backend (с процедурной генерацией):
cd /scratchpad && python backend.py

# В другой вкладке — новый Qwen сервер:
python backend_qwen.py
```

Затем в `frontend/src/App.tsx` можно переключаться между режимами:

- **Mode "Qwen"**: отправляет запрос на `http://localhost:8080/generate`
- **Mode "Pillow"**: использует старый `/api/generate` с процедурной генерацией

---

## 🔧 Настройка промпта

Измените строку в `backend_qwen.py`:

```python
prompt = f"{selected_style_description} photorealistic, high detail, 8k resolution, full body"
```

Примеры для разных стилей:

| Стиль | Промпт |
|-------|--------|
| Bob haircut | "bob haircut with ash gray hair, photorealistic, side profile view, soft lighting" |
| Hollywood waves | "long wavy hair swept to one side, ash gray color, elegant evening look" |
| High bun | "high textured bun hairstyle with volume at roots and loose face-framing strands" |

---

## 🧪 Тест через curl

```bash
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "image": "http://localhost:3000/preview.jpg",
    "prompt": "ash gray bob haircut, photorealistic"
  }'
```

---

## 📊 Требования к железу

- **GPU с CUDA** (рекомендуется): RTX 3060+ или A100 — генерация за ~5–15 сек
- **CPU only**: работает медленнее (~30–60 сек на изображение)
- **RAM**: минимум 12 ГБ свободной памяти

---

## 🐛 Возможные ошибки и решения

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `ModuleNotFoundError: transformers` | Не установлены зависимости | `pip install transformers torch...` |
| `Model not found` | Модель не скачана | Запустите `huggingface-cli download ...` |
| CUDA OOM (Out Of Memory) | Недостаточно VRAM | Уменьшите resolution или используйте CPU |
| `ValueError: Image must have mode 'RGB'` | Alpha-канал в изображении | Добавьте `.convert("RGB")` |

---

## 🚀 Рекомендации по производительности

```bash
# Для быстрой работы на GPU:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Квантование модели (меньше VRAM, чуть меньше качество):
python -c "from transformers import AutoModelForImageToImage; model = AutoModelForImageToImage.from_pretrained('./models/qwen-image-v1.5', device_map='auto')"
```

---

## 📝 Примечания

- Модель Qwen Image 2.5 использует архитектуру **LLaVA-style** (текст + image → изображение)
- Она понимает промпты на английском языке лучше, чем на русском
- Для лучших результатов используйте промпты: `"ash gray bob haircut photorealistic"` вместо русского текста