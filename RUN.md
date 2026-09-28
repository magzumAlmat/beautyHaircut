# 📋 Инструкция по запуску сервиса Beauty Haircut

## ⚡ Быстрый старт (запуск на порту 8000)

### Шаг 1: Установите Python зависимости для backend

```bash
pip install fastapi uvicorn pillow numpy requests transformers torch torchvision
```

### Шаг 2: Запустите backend

В **новой терминальной вкладке**:

```bash
cd scratchpad
python backend.py
```

Сервер запустится на `http://localhost:8001`.

Вы должны увидеть в консоли:

```text
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

### Шаг 3: Запустите frontend

В **другой терминальной вкладке**:

```bash
cd scratchpad/frontend
npm install
npm run dev
```

Сервер запустится на `http://localhost:3000`.

---

## ✅ Проверка работоспособности

1. Откройте браузер и перейдите на `http://localhost:3000`
2. Загрузите любое фото (портрет)
3. Выберите стиль "Каре / Боб-каре" или любой другой из списка
4. Нажмите кнопку **"Применить"**
5. Дождитесь генерации — результат появится в предпросмотре

---

## 🤖 Настройка Qwen Image 2.1 (опционально)

Если вы хотите использовать нейросеть Qwen Image 2.1 вместо процедурной генерации:

### 1. Скачайте и установите модель

```bash
# В новой терминальной вкладке:
pip install transformers torch torchvision --index-url https://download.pytorch.org/whl/cu121

python -c "
from transformers import AutoModelForImage2Image, AutoProcessor
import torch

model_id = './models/qwen-image-v1.5'  # или путь к вашему скачанному репозиторию

processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForImage2Image.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map='auto',
    low_cpu_mem_usage=True,
).eval()

print('✅ Qwen Image 2.1 успешно загружена!')
"
```

### 2. Активируйте в backend.py

Откройте `scratchpad/backend.py` и найдите строку:

```python
QWEN_ENABLE = False
```

Измените на:

```python
QWEN_ENABLE = True
```

Перезапустите backend:

```bash
# Перезапуск сервера
kill $(lsof -t:i8001) 2>/dev/null || true
cd scratchpad && python backend.py
```

### 3. Проверка работы Qwen

После перезапуска backend должен вывести в консоль:

```text
INFO:     Qwen Image 2.1 модель готова!
```

Теперь при генерации сервис будет использовать нейросеть вместо процедурной генерации через Pillow.

---

## 🧪 Локальный тест через curl

Запустите отдельным процессом в одной из вкладок:

```bash
curl -X POST http://localhost:8001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"image":"http://localhost:3000/preview.jpg","style_id":"bob","color":"ash_gray"}'
```

---

## 🐳 Docker (опционально)

**Dockerfile:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY backend.py .
COPY frontend/ ./frontend/

# В папке проекта создайте файл docker-compose.yml или запустите отдельно:
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8001:8001"
    volumes:
      - ./outputs:/app/outputs
    environment:
      - QWEN_ENABLE=true

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:3000"
```

---

## 📝 Примечания к работе

- Backend работает на порту **8001**, frontend — на **3000**.
- Результаты генерации сохраняются в `scratchpad/outputs/qwen/` и `scratchpad/outputs/pillow/`.
- При использовании Qwen Image 2.1 изображения сохраняются с расширением `.png`, при fallback через Pillow — также `.png`.
