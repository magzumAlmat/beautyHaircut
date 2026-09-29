# ✂️ Beauty Haircut Generator

Сервис для генерации причесок с пепельными волосами.

## 🚀 Как запустить

### Backend (Python) — порт 8001

```bash
cd /Users/billionare/.lmstudio/apps/bionic/projects/d49037d8-47f4-5808-9028-c707de117f8f/workspace/scratchpad
python backend.py &
```

Backend будет доступен на `http://localhost:8001`

Проверка работоспособности:
```bash
curl http://localhost:8001/health
# {"status":"ok","timestamp":"2026-09-29T..."}
```

### Frontend (React + Vite) — порт 5173

```bash
cd /Users/billionare/.lmstudio/apps/bionic/projects/d49037d8-47f4-5808-9028-c707de117f8f/workspace/scratchpad/frontend
npm run dev --host 0.0.0.0
```

Frontend будет доступен на `http://localhost:5173`

---

## 📋 Функционал

- **Загрузка фото** через drag&drop или клик
- **Выбор прически** из 14 стилей в 3 категории:
  - Вечерние и торжественные (Голливудские волны, Пучок, Греческая коса, Французский твист)
  - Салонные укладки (Брашинг-объем, Пляжные волны, Эффект "влажных волос", Хвост, Пудровый пучок)
  - Трендовые стрижки (Каре, Каскад, Пикси, Вулфкат)
- **Генерация** через Pillow (процедурная генерация) или Qwen Image 2.1

---

## 🧠 Модели

### Pillow Fallback (работает сразу)
Процедурная генерация с помощью `PIL` — создаёт изображение пепельных волос с текстурой "боб". Работает без установки дополнительных зависимостей.

### Qwen Image 2.1 (опционально)
Для использования нейросетевой модели нужно:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers accelerate xformers
git clone https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct ./models/qwen-image-v1.5
```

Затем переключить режим в интерфейсе на "Qwen Image 2.1".

---

## 📁 Структура проекта

```
scratchpad/
├── backend.py              # FastAPI сервер (порт 8001)
├── frontend/               # React + Vite приложение (порт 5173)
│   ├── src/
│   │   ├── App.tsx        # Главный компонент
│   │   └── components/    # UploadSection, StyleSelector, PreviewSection
│   └── vite.config.ts     # Конфиг сборки
├── server.py              # Простой HTTP сервер (старый fallback)
└── LAUNCH.md             # Этот файл
```

---

## 🔧 API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/health` | Проверка работы сервера |
| `POST` | `/api/generate` | Генерация прически |
| `POST` | `/api/upload` | Загрузка изображения |
| `GET`  | `/api/image/{id}` | Получение результата |

---

## 🧪 Пример запроса к API

```bash
curl -X POST http://localhost:8001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/png;base64,...", "style_id": "bob"}'
```

---

## 🌐 GitHub

https://github.com/magzumAlmat/beautyHaircut

---

**Автор**: magzumAlmat