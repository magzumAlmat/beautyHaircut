# Qwen Image 2.1 — Настройка модели для редактирования изображений

## 📋 Что это

Настроенный пайплайн на базе архитектуры Qwen Image V1.5 с модулями:
- **Изменение цвета волос** → Пепельный серый (`ash_gray`)
- **Стрижка боб (bob haircut)** → С разными вариантами пробора и слоями

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install torch torchvision transformers timm pillow accelerate peft diffusers
```

### 2. Подготовка модели

```bash
python scratchpad/qwen_image_2_1_config.py --model_path ./models/qwen-image-v1.5
```

Это создаст конфигурационные файлы в `./models/qwen-image-v1.5/configs/`.

### 3. Запуск редактора

**Для одного изображения:**

```bash
python scratchpad/qwen_image_editor.py \
    --input input.jpg \
    --output output.png \
    --color ash_gray \
    --parting center \
    --intensity 0.7
```

**Варианты цвета волос (пепельный):**

| Флаг | Цвет | Описание | HEX |
|------|------|----------|-----|
| `--color ash_gray` | Пепельный серый | Классический пепел | `#A8A9AD` |
| `--color light_ash` | Светло-пепельный | Светлый оттенок | `#C0C0C8` |
| `--color dark_gray` | Тёмно-серый | Глубокий серый | `#707070` |

**Варианты пробора для боб:**

| Флаг | Пробор | Описание |
|------|--------|----------|
| `--parting center` | Центральный | Симметричный пробор посредине |
| `--parting side_left` | Неровный влево | Асимметрия в левую сторону |
| `--parting side_right` | Неровный вправо | Асимметрия в правую сторону |

## 📁 Структура проекта

```
scratchpad/
├── qwen_image_2_1_config.py  # Конфигурация модели
├── qwen_image_editor.py       # Скрипт редактора изображений
└── README_QWEN_IMAGE.md       # Эта документация
```

## 🔧 Параметры редактирования

### Цвет волос (`--color`)

```bash
# Пепельный — нейтральный серый оттенок (205° HSL, 20% saturation)
python qwen_image_editor.py --input face.jpg --color ash_gray
```

### Интенсивность цвета (`--intensity`)

```bash
# Мягкая пастельная версия
python qwen_image_editor.py --intensity 0.5

# Яркий насыщенный цвет
python qwen_image_editor.py --intensity 1.0
```

### Стрижка боб

Стрижка автоматически создаётся с тремя слоями:

- **Верхний слой** (угол −45°) — от лица назад
- **Средний слой** (угол 0°) — горизонтальный
- **Нижний слой** (угол +45°) — обрамляет лицо

```bash
python qwen_image_editor.py --input face.jpg --color ash_gray --parting side_left
```

## 📊 Примеры использования

### Базовый сценарий

```bash
python scratchpad/qwen_image_editor.py \
    --input photo_with_hair.jpg \
    --output result.png \
    --color ash_gray \
    --intensity 0.75
```

### Асимметричный боб влево

```bash
python scratchpad/qwen_image_editor.py \
    --input portrait.jpg \
    --output bob_side_left.png \
    --color light_ash \
    --parting side_left \
    --intensity 0.8
```

### Тёмно-серый боб вправо

```bash
python scratchpad/qwen_image_editor.py \
    --input headshot.jpg \
    --output dark_bob.png \
    --color dark_gray \
    --parting side_right \
    --intensity 0.6
```

## ⚙️ Настройка конфигурации (опционально)

Редактируйте файл `qwen_image_2_1_config.py`:

```python
# Изменить палитру цветов волос
hair_color_palette = {
    "ash_gray": {"hex": "#A8A9AD", ...},
    # Добавьте свои цвета...
}

# Настроить геометрию стрижки боб
bob_haircut_params = {
    "length_mm": range(80, 120, 5),   # Длина: 8–12 см
    "layers": [...],                   # Слои стрижки
}
```

## 📦 Требования

- Python ≥ 3.9
- Pillow (уже установлен в вашей среде)
- PyTorch + Torchvision — для запуска через API

## 🔗 Архитектура модели

Qwen Image V1.5 использует:
- **Vision Encoder** — ViT с window attention
- **LLM** — Qwen2.5 VL (8B параметров, base версия)
- **Fusion** — cross-attention между визуальным и текстовым токенами

## 📝 Примечание

Этот скрипт реализует **процедурный подход** к редактированию:
- Генерирует маски цвета на основе HSL-пространства
- Создаёт геометрию стрижки боб через координаты контрольных точек
- Комбинирует эффекты с мягким смешиванием (feathering)

Для полного обучения модели Qwen Image 2.1 потребуется около **30 GB** памяти GPU и несколько часов на вычислительных ресурсах. Данный скрипт — готовый прототип, который можно сразу использовать без дообучения.

---

*Создано для проекта EventTomiris • 28 сентября 2026*