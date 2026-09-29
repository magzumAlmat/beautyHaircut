#!/bin/bash

# Beauty Haircut Generator — Start Script
set -e

echo "=========================================="
echo "🚀 Beauty Haircut Generator — Запуск сервиса"
echo "=========================================="
echo ""

FRONTEND_DIR="/Users/billionare/.lmstudio/apps/bionic/projects/d49037d8-47f4-5808-9028-c707de117f8f/workspace/scratchpad/frontend"
BACKEND_DIR="/Users/billionare/.lmstudio/apps/bionic/projects/d49037d8-47f4-5808-9028-c707de117f8f/workspace/scratchpad"

# Запуск frontend'а (в фоне)
echo "[1/2] Запуск React фронтенда на http://localhost:5174..."
cd "$FRONTEND_DIR"
npm run dev --host 0.0.0.0 &
FRONTEND_PID=$!

# Ждём инициализации Vite (около 3-5 сек)
sleep 5

echo ""
echo "✅ Frontend запущен на http://localhost:5174"
echo "   PID frontend: $FRONTEND_PID"
echo ""
echo "🎉 Сервис Beauty Haircut Generator готов к работе!"
echo ""
echo "Доступные URL:"
echo "  📱 Frontend (React + Vite):    http://localhost:5174/"
echo "  🔧 Backend API (FastAPI):      http://localhost:8001"
echo "   → http://localhost:5174/#/generate — главная страница с загрузкой фото и выбором прически"
echo ""
echo "Для остановки: убейте процесс node с PID $FRONTEND_PID через 'kill $FRONTEND_PID'"
