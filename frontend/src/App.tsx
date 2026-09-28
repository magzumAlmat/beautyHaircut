import React, { useState } from 'react';
import UploadSection from './components/UploadSection';
import StyleSelector from './components/StyleSelector';
import PreviewSection from './components/PreviewSection';
import type { Style, File as ReactFile } from './types';

const styles: Style[] = [
  { id: 'hollywood', name: 'Голливудские волны', subtitle: 'Гладкие крупные локоны на одну сторону', category: 'вечерние' },
  { id: 'high_bun', name: 'Высокий текстурный пучок', subtitle: 'Элегантная собранная прическа с объемом у корней', category: 'вечерние' },
  { id: 'low_bun', name: 'Низкий гладкий пучок', subtitle: 'Строгий минималистичный вариант', category: 'вечерние' },
  { id: 'greek_braid', name: 'Греческая коса', subtitle: 'Пышное объемное плетение переходящее в хвост', category: 'вечерние' },
  { id: 'french_twist', name: 'Французский твист (ракушка)', subtitle: 'Классический вертикальный валик на затылке', category: 'вечерние' },
  { id: 'blowout', name: 'Брашинг-объем', subtitle: 'Пышная укладка феном и круглой щеткой', category: 'салонные' },
  { id: 'beach_waves', name: 'Пляжные волны (Beach Waves)', subtitle: 'Расслабленные небрежные текстурные локоны', category: 'салонные' },
  { id: 'wet_hair', name: 'Эффект влажных волос', subtitle: 'Трендовая подиумная укладка с гелем', category: 'салонные' },
  { id: 'high_ponytail', name: 'Высокий текстурный хвост', subtitle: 'Объемный хвост с начесом или легкой завивкой', category: 'салонные' },
  { id: 'straight_hair', name: 'Идеально прямые волосы', subtitle: 'Вытянутые утюжком пряди с глянцевым блеском', category: 'салонные' },
  { id: 'bob', name: 'Каре / Боб-каре', subtitle: 'Классическое каре или боб с удлинением', category: 'стрижки' },
  { id: 'cascade', name: 'Каскад и Лесенка', subtitle: 'Многоступенчатые стрижки для объема на средние волосы', category: 'стрижки' },
  { id: 'pixie', name: 'Пикси', subtitle: 'Короткая динамичная стрижка с рваными прядями', category: 'стрижки' },
  { id: 'wolfcut', name: 'Вулфкат (Wolfcut) / Шегги', subtitle: 'Текстурные многослойные растрепанные стрижки', category: 'стрижки' },
];

const categories = [
  { id: 'all', label: 'Все' },
  { id: 'вечерние', label: 'Вечерние и торжественные' },
  { id: 'салонные', label: 'Салонные укладки' },
  { id: 'стрижки', label: 'Трендовые стрижки' },
];

function App() {
  const [selectedStyle, setSelectedStyle] = useState<Style | null>(null);
  const [imageFile, setImageFile] = useState<ReactFile | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [resultUrl, setResultUrl] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [generationMode, setGenerationMode] = useState<'pillow' | 'qwen'>('qwen');

  function handleImageUpload(file: File): void {
    setImageFile({ name: file.name, size: file.size });
    setPreviewUrl(URL.createObjectURL(file));

    if (file.size > 10 * 1024 * 1024) {
      alert('Файл слишком большой. Максимальный размер: 10 MB');
      setImageFile(null); setPreviewUrl(null); return;
    }

    const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      alert('Поддерживаются только JPG, PNG и WebP');
      setImageFile(null); setPreviewUrl(null); return;
    }
  }

  async function applyStyle(styleId: string): Promise<void> {
    if (!selectedStyle || !imageFile || !previewUrl) return;
    setIsProcessing(true);

    try {
      let resultUrl: string | null = null;

      if (generationMode === 'qwen' && window.qwenImageModel) {
        // Использование Qwen Image 2.1 модели
        const prompt = `Измени цвет волос на пепельный и создай прическу "${selectedStyle.name}". Сделай ${selectedStyle.subtitle}.`;
        
        try {
          console.log(`Вызов Qwen Image 2.1: ${prompt}`);
          
          // Попытка использовать модель Qwen Image 2.1
          const qwenResult = await window.qwenImageModel.generate({
            image: previewUrl,
            prompt: prompt,
            size: "1024x1024",
            steps: 30,
            guidance_scale: 7.5,
          });

          if (qwenResult && qwenResult.url) {
            resultUrl = qwenResult.url;
            console.log('Qwen Image 2.1 результат:', qwenResult);
          } else if (qwenResult?.images?.[0]) {
            // Если модель возвращает base64 или blob
            const imgData = typeof qwenResult.images[0] === 'string' 
              ? qwenResult.images[0]
              : URL.createObjectURL(qwenResult.images[0]);
            resultUrl = imgData;
          }

        } catch (qwenError) {
          console.warn('Qwen Image 2.1 недоступна, используем fallback:', qwenError);
        }
      }

      // Fallback на процедурную генерацию через backend (Pillow)
      if (!resultUrl) {
        const response = await fetch('http://localhost:8001/api/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image: previewUrl, style_id: styleId, color: 'ash_gray' }),
        });

        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        resultUrl = data.result_url;
      }

      setResultUrl(resultUrl);
    } catch (error) {
      console.error('Ошибка генерации:', error);
      alert('Не удалось связаться с backend сервером. Показан предпросмотр.');
    } finally {
      setIsProcessing(false);
    }
  }

  function handleDownload(): void {
    if (!resultUrl) return;
    
    const link = document.createElement('a');
    link.href = resultUrl;
    link.download = `haircut-${selectedStyle?.id || 'unknown'}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-950 to-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-slate-900/60 border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 bg-clip-text text-transparent">
            ✂️ Beauty Haircut Generator
          </h1>

          {/* Кнопка переключения режима генерации */}
          <div className="flex items-center gap-3">
            <span className="text-sm text-slate-400">Модель:</span>
            <button
              onClick={() => setGenerationMode('qwen')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                generationMode === 'qwen'
                  ? 'bg-purple-600/30 text-purple-300 border border-purple-500/50'
                  : 'bg-slate-800/50 text-slate-400 border border-slate-700'
              }`}
            >
              Qwen Image 2.1 🤖
            </button>
            <button
              onClick={() => setGenerationMode('pillow')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                generationMode === 'pillow'
                  ? 'bg-blue-600/30 text-blue-300 border border-blue-500/50'
                  : 'bg-slate-800/50 text-slate-400 border border-slate-700'
              }`}
            >
              Pillow (Fallback) 🖼️
            </button>

            {/* Статус модели */}
            <div className="ml-2 px-3 py-1.5 rounded-full text-xs font-medium bg-slate-800/50 border border-slate-700">
              {window.qwenImageModel ? (
                <span className="text-green-400 flex items-center gap-1.5">
                  ● Qwen Image 2.1 готова
                </span>
              ) : (
                <span className="text-yellow-400 flex items-center gap-1.5">
                  ⚠️ Модель не загружена
                </span>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Левая колонка — загрузка и выбор */}
          <div className="space-y-6">
            <UploadSection onImageUpload={handleImageUpload} />

            <StyleSelector
              styles={styles.filter((s) =>
                selectedStyle ? s.category === selectedStyle.category : true
              )}
              selectedStyle={selectedStyle}
              onSelect={(styleId: string) => setSelectedStyle(styles.find((s) => s.id === styleId) || null)}
            />

            {/* Инструкция по запуску Qwen Image 2.1 */}
            <div className="bg-slate-800/30 border border-white/5 rounded-xl p-4">
              <h3 className="text-sm font-semibold text-purple-300 mb-2 flex items-center gap-2">
                🚀 Как запустить Qwen Image 2.1:
              </h3>
              <pre className="text-xs text-slate-400 overflow-x-auto whitespace-pre-wrap font-mono bg-black/50 rounded p-3">
{`# Установить модель (в python):
pip install transformers torch

# В backend.py заменить класс HairStyleGenerator на:
from transformers import AutoModelForImage2Image, AutoProcessor
import torch

class QwenImageGenerator:
    def __init__(self, model_path="./models/qwen-image-v1.5"):
        self.model = AutoModelForImage2Image.from_pretrained(model_path, device_map="auto", torch_dtype=torch.float16)
        self.processor = AutoProcessor.from_pretrained(model_path)

    def generate(self, image_url: str, prompt: str):
        """Генерирует изображение с Qwen Image 2.1."""
        from PIL import Image
        import base64, io

        # Загрузить изображение
        response = requests.get(image_url)
        img = Image.open(io.BytesIO(response.content))

        # Преобразовать в tensor
        inputs = self.processor(text=prompt, images=img, return_tensors="pt").to(self.model.device)
        
        # Генерация
        with torch.no_grad():
            generated_images = self.model.generate(
                **inputs,
                num_images_per_prompt=1,
                negative_prompt="bad quality, blurry",
                max_new_tokens=256,
            )

        return generated_images[0].cpu().numpy()


# В backend.py заменить HairStyleGenerator на QwenImageGenerator:
generator = QwenImageGenerator()
def generate_with_qwen(self, img_path_or_base64, style_id, color):
    """Использует Qwen Image 2.1 для генерации прически."""
    prompt = self.STYLES[style_id]["prompt"]
    result = generator.generate(img_path_or_base64, prompt)
    
    # Сохранить результат
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{color}_{style_id}_{int(time.time())}.png"
    img_save_path = output_dir / filename
    Image.fromarray(result).save(img_save_path)
    
    return {
        "result_url": f"http://localhost:8001/outputs/{filename}",
        "model": "qwen-image-2.1",
        "prompt": prompt,
    }`}
              </pre>
            </div>
          </div>

          {/* Правая колонка — предпросмотр */}
          <PreviewSection
            imageFile={imageFile}
            previewUrl={previewUrl}
            selectedStyle={selectedStyle}
            resultUrl={resultUrl}
            isProcessing={isProcessing}
            onApply={() => {}}
            onDownload={handleDownload}
            mode={generationMode}
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 mt-8">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-slate-500 text-sm">
          Beauty Haircut Generator — Qwen Image 2.1 Integration Demo
        </div>
      </footer>
    </div>
  );
}

export default App;