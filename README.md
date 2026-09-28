# 🪄 Beauty Haircut — Генератор причесок с Qwen Image 2.1

Веб-сервис для изменения цвета волос на **пепельный (ash gray)** и создания стрижки **боб (bob haircut)**. Приложение позволяет загружать фото, выбирать из **14 причесок** и применять их к изображению.

## 🌟 Особенности

- ✨ Изменение цвета волос на пепельный
- ✂️ 14 стилей причесок в 3 категориях:
  - **Вечерние и торжественные:** голливудские волны, высокий пучок, низкий пучок, греческая коса, французский твист
  - **Салонные укладки:** брашинг-объем, пляжные волны, эффект влажных волос, хвост, прямые волосы
  - **Трендовые стрижки:** каре/боб, каскад, пикси, волфкат (wolfcut)
- 🤖 Интеграция с **Qwen Image 2.1** для генерации реалистичных изображений
- 🎨 Процедурная генерация через Pillow как fallback

---

## 🚀 Быстрый старт

```bash
# 1️⃣ Запустить backend (порт 8001)
cd scratchpad
pip install -r requirements.txt
python backend.py

# 2️⃣ Запустить frontend (порт 3000)
cd frontend
npm install
npm run dev

# 3️⃣ Открыть в браузере
http://localhost:3000
```

---

## 📁 Структура проекта

```
scratchpad/
├── backend.py              # FastAPI сервер (порт 8001) — API для генерации
├── server.py               # Простой HTTP сервер на стандартном Python (альтернатива)
├── requirements.txt        # Python зависимости
├── README.md               # Документация проекта
│
├── frontend/              # React + Vite + Tailwind
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── App.tsx                ← ГЛАВНЫЙ КОМПОНЕНТ (все в одном файле)
│       ├── main.tsx              # Entry point
│       └── components/
│           ├── UploadSection.tsx    ← Загрузка фото + превью
│           ├── StyleSelector.tsx   ← Выбор из 14 причесок с SVG иконками
│           └── PreviewSection.tsx   ← Предпросмотр + кнопка "Применить"
├── docs/                    # Документация
│   └── QWEN_SETUP.md       ← Инструкция по установке Qwen Image 2.1
└── models/                  # Папка для скачанных моделей (qwen-image-v1.5)
```

---

## 🤖 Настройка Qwen Image 2.1

1. **Скачайте модель:**

   ```bash
   pip install transformers torch torchvision
   python -c "from transformers import AutoModelForImage2Image, AutoProcessor; model = AutoModelForImage2Image.from_pretrained('./models/qwen-image-v1.5', device_map='auto')"
   ```

2. **Активируйте в `backend.py`:**

   Откройте `scratchpad/backend.py` и измените:

   ```python
   QWEN_ENABLE = False  # ← поменяйте на True после установки модели
   ```

3. **Перезапустите backend:**

   ```bash
   python backend.py
   ```

Теперь при генерации сервис будет использовать Qwen Image 2.1 вместо процедурной генерации.

---

## 🧪 Локальный тест через curl

```bash
curl -X POST http://localhost:8001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"image":"data:image/png;base64,iVBORw0KGgo...", "style_id":"bob", "color":"ash_gray"}'
```

---

## 📋 API Reference

### POST `/api/generate` — Генерация прически

**Тело запроса:**

| Поле | Тип | Описание |
|------|-----|----------|
| `image` | string | URL изображения или base64-encoded PNG/JPG/WebP |
| `style_id` | string | ID стиля (см. таблицу ниже) |
| `color` | string | Цвет волос: `"ash_gray"` (пепельный), `"platinum"`, `"light_ash"` и др. |

**Пример ответа:**

```json
{
  "success": true,
  "style_id": "bob",
  "color": "ash_gray",
  "result_url": "/api/download/bob_ash_gray_1735456789.png",
  "metadata": {
    "generated_at": "2026-09-28T17:19:32.123456Z",
    "hash": "bob_ash_gray_1735456789"
  }
}
```

### GET `/api/download/{filename}` — Скачать результат

### GET `/api/styles` — Получить список всех стилей

---

## 📋 Полный список причесок (14 стилей)

| ID | Название | Описание |
|----|----------|----------|
| `hollywood` | Голливудские волны | Гладкие, крупные, идеально синхронные локоны на одну сторону |
| `high_bun` | Высокий текстурный пучок | Элегантная собранная прическа с объемом у корней и легкими прядями у лица |
| `low_bun` | Низкий гладкий пучок | Строгий, минималистичный вариант, создающий лаконичный образ |
| `greek_braid` | Греческая коса | Пышное объемное плетение, плавно переходящее в хвост |
| `french_twist` | Французский твист (ракушка) | Классический вертикальный валик на затылке |
| `blowout` | Брашинг-объем | Пышная укладка феном и круглой щеткой |
| `beach_waves` | Пляжные волны (Beach Waves) | Расслабленные, слегка небрежные текстурные локоны |
| `wet_hair` | Эффект «влажных волос» | Трендовая подиумная укладка с помощью геля |
| `high_ponytail` | Высокий текстурный хвост | Объемный хвост с начесом или легкой завивкой |
| `straight_hair` | Идеально прямые волосы | Вытянутые утюжком пряди с глянцевым блеском |
| `bob` | Каре / Боб-каре | Классическое каре, боб-каре или с удлинением |
| `cascade` | Каскад и Лесенка | Многоступенчатые стрижки для объема на средние и длинные волосы |
| `pixie` | Пикси | Короткая, динамичная стрижка с рваными прядями |
| `wolfcut` | Вулфкат (Wolfcut) / Шегги | Текстурные, намеренно растрепанные многослойные стрижки |

---

## 🎨 Цвета волос

- `ash_gray` — пепельный (RGB: 168, 169, 173)
- `light_ash` — светлый пепельный
- `dark_gray` — темный пепельный
- `platinum` — платиновый блонд
- `ebony_gray` — угольно-серый

---

## 🔧 Архитектура решения

### Backend (`backend.py`)

- **Endpoint** `/api/generate` принимает `{ image, style_id, color }`
- Сначала пробует сгенерировать через Qwen Image 2.1 (если `QWEN_ENABLE=True` и модель установлена)
- Если Qwen недоступен → используется процедурная генерация через Pillow
- Возвращает JSON с `result_url`

### Frontend (`frontend/src/App.tsx`)

Один файл содержит всю логику: состояние загрузки фото, выбор стиля, отправка запроса на `/api/generate`, отображение результата. Используется Tailwind CSS для стилизации (темная тема, градиенты).

---

## 🐳 Docker (опционально)

```dockerfile
FROM python:3.12-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend.py .
WORKDIR /app
CMD ["python", "backend.py"]
```

---

## ✅ Чеклист перед продакшном

- [ ] Qwen Image 2.1 скачана и установлена в `./models/qwen-image-v1.5`
- [ ] `QWEN_ENABLE = True` в `backend.py`
- [ ] Настроен CORS для домена приложения (не `*`)
- [ ] Проверена обработка больших изображений (> 4K) — возможно, нужно добавить ресайз
- [ ] Добавлена обработка ошибок сети при отправке запроса на backend

---

## 📝 Примечания

- Backend работает на порту **8001** (FastAPI + Pillow)
- Frontend — порт **3000** (Vite + React)
- Результаты сохраняются в `outputs/` (субпапки `qwen/` и `pillow/`)
- Цвет волос по умолчанию: пепельный (`ash_gray`: RGB 168, 169, 173)
