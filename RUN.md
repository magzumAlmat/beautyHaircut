# Hair Style Selector — Запуск сервиса

## Быстрый старт

### 1. Backend (порт 8001)

```bash
cd /Users/billionare/.lmstudio/apps/bionic/projects/d49037d8-47f4-5808-9028-c707de117f8f/workspace/scratchpad
python backend.py
```

Backend запустится на `http://localhost:8001`

### 2. Frontend (порт 3000)

В **новом терминале**:

```bash
cd /Users/billionare/.lmstudio/apps/bionic/projects/d49037d8-47f4-5808-9028-c707de117f8f/workspace/scratchpad/frontend
npm install
npm run dev
```

Frontend запустится на `http://localhost:3000`

## Проверка работоспособности backend'a

```bash
curl http://localhost:8001/health
# Ответ: {"status":"ok", "service":"Hair Style Selector API"}
```

## Логи

- Backend логи → `/tmp/backend.log`
- Frontend логи — в консоли браузера (F12) и в терминале `npm run dev`

## Структура

```
scratchpad/
├── backend.py              # FastAPI сервер (порт 8001)
├── frontend/               # React + Vite приложение
│   ├── src/
│   │   ├── App.tsx        # Главный компонент
│   │   └── components/    # Компоненты UI
│   └── package.json
└── outputs/                # Сгенерированные изображения
```

## API Endpoints

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/health` | GET | Пинг сервера |
| `/api/generate` | POST | Генерация прически |
| `/api/download/{filename}` | GET | Скачивание результата |
| `/api/styles` | GET | Список доступных стилей |

## Пример запроса

```bash
curl -X POST http://localhost:8001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"image":"data:image/png;base64,iVBORw...", "style_id":"bob", "color":"ash_gray"}'
```
