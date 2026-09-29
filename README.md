# ✂️ Beauty Haircut Generator

Веб-сервис для изменения цвета волос на **пепельный (ash gray)** и создания причесок.

## 🌟 Особенности

- ✨ Изменение цвета волос на пепельный
- ✂️ 14 стилей причесок в 3 категориях:
  - **Вечерние и торжественные:** голливудские волны, высокий пучок, низкий пучок, греческая коса, французский твист
  - **Салонные укладки:** брашинг-объем, пляжные волны, эффект влажных волос, хвост, прямые волосы, пудровый пучок
  - **Трендовые стрижки:** каре/боб, каскад, пикси, волфкат (wolfcut)
- 🤖 Интеграция с **Qwen Image 2.1** для генерации реалистичных изображений
- 🎨 Процедурная генерация через Pillow как fallback

---

## 🚀 Быстрый старт

```bash
# 1️⃣ Запустить backend (порт 8001) — опционально, если нужен API
cd /Users/billionare/.lmstudio/apps/bionic/projects/d49037d8-47f4-5808-9028-c707de117f8f/workspace/scratchpad
python server.py

# 2️⃣ Запустить frontend (порт 5174) — React + Vite
cd /Users/billionare/.lmstudio/apps/bionic/projects/d49037d8-47f4-5808-9028-c707de117f8f/workspace/scratchpad/frontend
npm install
npm run dev --host 0.0.0.0

# 3️⃣ Открыть в браузере
http://localhost:5174
```

---

## 📁 Структура проекта

```
scratchpad/
├── server.py              # HTTP сервер (Pillow fallback) — порт 8001
├── backend.py             # FastAPI сервер с Qwen Image 2.1 интегрирован
├── start.html            # HTML-страница для запуска сервиса
├── test.html             # Тестовая страница API
├── README.md              # Документация проекта
├── requirements.txt       # Python зависимости (fastapi, pillow)
└── frontend/             # React + Vite + Tailwind
    ├── package.json      # Зависимости frontend'а
    ├── vite.config.ts    # Конфиг Vite
    └── src/
        ├── App.tsx       ← ГЛАВНЫЙ КОМПОНЕНТ (все в одном файле)
        ├── main.tsx
        ├── types.ts
        └── components/
            ├── UploadSection.tsx      # Drag&drop загрузка фото
            ├── StyleSelector.tsx      # Выбор прически из 14 стилей
            └── PreviewSection.tsx     # Предпросмотр + кнопки
```

---

## 🧠 Архитектура решения

**Backend (порт 8001):**
- `server.py` — простой HTTP сервер на Python, использующий Pillow для процедурной генерации пепельных волос
- `backend.py` — FastAPI сервер с интеграцией Qwen Image 2.1 (если модель загружена)

**Frontend (порт 5174):**
- React + Vite + TypeScript
- TailwindCSS для стилизации
- Drag&drop загрузка изображений
- Выбор из 14 причесок с категоризацией

---

## 🧪 Тестирование API

Откройте `test.html` в браузере и отправьте JSON запрос:

```json
{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg...",
  "style_id": "bob"
}
```

---

## 🛠️ Технологический стек

**Frontend:** React 19, Vite, TailwindCSS, TypeScript  
**Backend:** Python FastAPI / HTTP.server + Pillow, Qwen Image 2.5 (опционально)  

---

*Создано с помощью Bionic AI Assistant*