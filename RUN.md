# 🚀 Hair Style Selector — Как запустить

## ⏩ Быстрый старт (3 минуты)

### Шаг 1. Установите зависимости

```bash
cd scratchpad/frontend
npm install
```

### Шаг 2. Запустите backend-сервер

Откройте **новый терминал**:

```bash
cd scratchpad
python server.py
```

Вы увидите:

```
==================================================
🚀 Hair Style Selector API Server
   📡 API:      http://127.0.0.1:8001/health
   🎨 Frontend: http://localhost:3000  (React)
==================================================
```

**Сервер работает на порту `http://localhost:8001`**.

### Шаг 3. Запустите frontend-сервер

В том же или другом терминале:

```bash
cd scratchpad/frontend
npm run dev
```

Откроется браузер по адресу **`http://localhost:3000`**

---

## 🎨 Что можно делать в интерфейсе:

1. Загрузите фото с лицом/волосами (JPG, PNG, WEBP)
2. Выберите категорию причесок:
   - Вечерние и торжественные (5 стилей)
   - Салонные укладки (5 стилей)
   - Трендовые стрижки (4 стиля)
3. Нажмите на любую из 14 причесок — она подсветится
4. Нажмите **«🎨 Применить»** — сервер обработает запрос и вернёт результат

---

## 📋 Полный список причесок:

### Вечерние и торжественные (5):

| ID | Название | Описание |
|----|----------|----------|
| `hollywood` | Голливудские волны | Гладкие, крупные локоны на одну сторону |
| `high_bun` | Высокий текстурный пучок | Объем у корней + пряди у лица |
| `low_bun` | Низкий гладкий пучок | Строгий минималистичный образ |
| `greek_braid` | Греческая коса | Пышное плетение → хвост |
| `french_twist` | Французский твист (ракушка) | Классический валик на затылке |

### Салонные укладки (5):

| ID | Название | Описание |
|----|----------|----------|
| `blowout` | Брашинг-объем | Фен + круглая щетка |
| `beach_waves` | Пляжные волны | Небрежные текстурные локоны |
| `wet_hair` | Влажные волосы | Подиумная укладка гелем |
| `high_ponytail` | Высокий хвост | Объемный с начесом/завивкой |
| `straight_hair` | Прямые волосы | Утюжок + глянец |

### Трендовые стрижки (4):

| ID | Название | Описание |
|----|----------|----------|
| `bob` | Каре / Боб-каре | Классика или удлиненный боб |
| `cascade` | Каскад и Лесенка | Многоступенчатый объем |
| `pixie` | Пикси | Короткая с рваными прядями |
| `wolfcut` | Вулфкат / Шегги | Текстурные многослойные стрижки |

---

## 🔌 API для интеграции (если нужно):

### GET `/api/styles` — список всех стилей:

```json
[
  {"id": "bob", "name": "Каре / Боб-каре"},
  {"id": "pixie", "name": "Пикси"},
  {"id": "wolfcut", "name": "Вулфкат (Wolfcut) / Шегги"}
]
```

### POST `/api/generate` — генерация:

**Body:**

```json
{
  "image": "data:image/png;base64,iVBORw0KGgo...",
  "style_id": "bob",
  "color": "ash_gray"
}
```

**Ответ:**

```json
{
  "success": true,
  "style_id": "bob",
  "result_url": "/api/download/bob_ash_gray_20260928143502.png"
}
```

---

## 📦 Структура проекта:

```
scratchpad/
├── server.py              # Python HTTP-сервер (порт 8001)
│                          # — обрабатывает запросы /api/generate
├── backend.py             # FastAPI версия (альтернативная, тоже работает на 8001)
├── frontend/
│   ├── package.json       # React + Tailwind + Vite
│   ├── vite.config.ts
│   └── src/
│       ├── App.tsx        # Главный компонент
│       ├── main.tsx
│       └── components/
│           ├── UploadSection.tsx    — загрузка фото
│           ├── StyleSelector.tsx    — выбор из 14 причесок
│           └── PreviewSection.tsx   — предпросмотр + генерация
├── docker-compose.yml     # Docker Compose (если нужен)
├── requirements.txt       # Python зависимости
└── README.md
```

---

## 🐳 Docker (альтернативный способ запуска):

```bash
cd scratchpad
docker-compose up -d --build
```

Это запустит:
- Backend API на порту `8001`
- Frontend через Nginx на порту `80`

Откройте `http://localhost` в браузере.

---

## 🎯 Что делает сервер (`server.py`):

1. Принимает `POST /api/generate` с JSON: `{ image, style_id, color }`
2. Декодирует base64 изображение (или скачивает по URL)
3. Применяет процедурную генерацию прически через Pillow:
   - Маскирует область волос
   - Меняет цвет на пепельный (ASH GRAY)
   - Добавляет текстуру шума для реалистичности
4. Сохраняет результат в `scratchpad/outputs/{style}_{color}_timestamp.png`
5. Возвращает URL результата

---

## 🧪 Локальный тест через curl:

```bash
curl -X POST http://localhost:8001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/png;base64,iVBORw0KGgo...",
    "style_id": "bob",
    "color": "ash_gray"
  }'
```

---

## 🐛 Отладка:

- Проверьте статус API: `curl http://localhost:8001/health` → `{"status":"ok","service":"..."}`
- Получите список стилей: `GET http://localhost:8001/api/styles`

---

*Создано для проекта **EventTomiris** • Интеграция с Qwen Image 2.1*
