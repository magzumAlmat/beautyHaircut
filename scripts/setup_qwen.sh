#!/bin/bash
# 🤖 Установка Qwen Image 2.1 для Beauty Haircut
set -e

echo "📦 Устанавливаем зависимости..."
pip install transformers torch torchvision pillow requests huggingface_hub --quiet

echo ""
echo "📥 Скачиваем модель Qwen/Qwen2.5-Image-VL-Instruct..."
echo "   Это Image-to-Image модель от Alibaba Cloud."
echo ""

# Создаём папку для модели
mkdir -p models/qwen-image-v1.5

# Скачиваем модель через huggingface-cli
huggingface-cli download Qwen/Qwen2.5-Image-VL-Instruct \
    --local-dir ./models/qwen-image-v1.5 --repo-type model --force-download

echo ""
echo "✅ Модель скачана и установлена в: ./models/qwen-image-v1.5"
echo ""
ls -lh models/qwen-image-v1.5/ | head -20

# Проверяем размер модели
model_size=$(du -sh models/qwen-image-v1.5 2>/dev/null | cut -f1)
if [ -n "$model_size" ]; then
    echo "📊 Размер модели: $model_size"
fi

echo ""
echo "✅ Готово! Теперь можно запустить backend.py с QWEN_ENABLE=True"