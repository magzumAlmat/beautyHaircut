import React, { useState } from 'react';
import UploadSection from './components/UploadSection';
import StyleSelector from './components/StyleSelector';
import PreviewSection from './components/PreviewSection';
import type { Style, File as ReactFile } from './types';

const styles: Style[] = [
  { id: 'hollywood_waves', name: 'Голливудские волны', subtitle: 'Гладкие, крупные, идеально синхронные локоны на одну сторону', category: 'вечерние' },
  { id: 'high_bun', name: 'Высокий текстурный пучок', subtitle: 'Элегантная собранная прическа с объемом у корней и легкими прядями у лица', category: 'вечерние' },
  { id: 'low_bun', name: 'Низкий гладкий пучок', subtitle: 'Строгий, минималистичный вариант, создающий лаконичный образ', category: 'вечерние' },
  { id: 'greek_braid', name: 'Греческая коса', subtitle: 'Пышное объемное плетение, плавно переходящее в хвост', category: 'вечерние' },
  { id: 'french_twist', name: 'Французский твист (ракушка)', subtitle: 'Классический вертикальный валик на затылке', category: 'вечерние' },
  { id: 'brush_volume', name: 'Брашинг-объем', subtitle: 'Пышная укладка феном и круглой щеткой', category: 'салонные' },
  { id: 'beach_waves', name: 'Пляжные волны (Beach Waves)', subtitle: 'Расслабленные, слегка небрежные текстурные локоны', category: 'салонные' },
  { id: 'wet_hair', name: 'Эффект «влажных волос»', subtitle: 'Трендовая подиумная укладка с помощью геля', category: 'салонные' },
  { id: 'high_textured_ponytail', name: 'Высокий текстурный хвост', subtitle: 'Объемный хвост с начесом или легкой завивкой', category: 'салонные' },
  { id: 'pearl_bun', name: 'Пудровый пучок (Pearl Bun)', subtitle: 'Нежный пучок на макушке с мягкими, слегка небрежными прядями по бокам — элегантный вариант для офиса или свидания', category: 'салонные' },
  { id: 'bob', name: 'Каре / Боб-каре', subtitle: 'Классическое каре, боб-каре или с удлинением', category: 'стрижки' },
  { id: 'cascade', name: 'Каскад и Лесенка', subtitle: 'Многоступенчатые стрижки для объема на средние и длинные волосы', category: 'стрижки' },
  { id: 'pixie', name: 'Пикси', subtitle: 'Короткая, динамичная стрижка с рваными прядями', category: 'стрижки' },
  { id: 'wolfcut', name: 'Вулфкат (Wolfcut) / Шегги', subtitle: 'Текстурные, намеренно растрепанные многослойные стрижки', category: 'стрижки' },
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
  const [generationMode, setGenerationMode] = useState<'pillow' | 'qwen'>('pillow');

  function handleImageUpload(file: File): void {
    setImageFile({ name: file.name, size: file.size });
    setPreviewUrl(URL.createObjectURL(file));
  }

  async function applyStyle(style: Style): Promise<void> {
    if (!selectedStyle || !imageFile || !previewUrl) return;
    setIsProcessing(true);

    try {
      let resultUrl: string | null = null;

      const response = await fetch('http://localhost:8001/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: previewUrl, style_id: style.id }),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();

      if (data.error) {
        console.error('Ошибка генерации:', data.error);
        alert('Не удалось сгенерировать изображение. Показан предпросмотр.');
      } else if (data.result_url) {
        resultUrl = data.result_url;
      }

    } catch (error) {
      console.error('Ошибка соединения с backend:', error);
      alert('Не удалось связаться с backend сервером (порт 8001). Показан предпросмотр.');
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

  function handleReset(): void {
    setImageFile(null);
    setPreviewUrl(null);
    setResultUrl(null);
    setSelectedStyle(null);
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-950 to-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-slate-900/60 border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 bg-clip-text text-transparent">
            ✂️ Beauty Haircut Generator — Pearly Ash Gray Bob
          </h1>

          <div className="flex items-center gap-3">
            <span className="text-sm text-slate-400">Модель:</span>
            <button onClick={() => setGenerationMode('qwen')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${generationMode === 'qwen' ? 'bg-purple-600/30 text-purple-300 border border-purple-500/50' : 'bg-slate-800/50 text-slate-400 border border-slate-700'}`}>Qwen Image 2.1 🤖</button>
            <button onClick={() => setGenerationMode('pillow')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${generationMode === 'pillow' ? 'bg-blue-600/30 text-blue-300 border border-blue-500/50' : 'bg-slate-800/50 text-slate-400 border border-slate-700'}`}>Pillow (Fallback) 🖼️</button>
            <div className="ml-2 px-3 py-1.5 rounded-full text-xs font-medium bg-slate-800/50 border border-slate-700">✨ 14 причесок • Пепельный цвет волос</div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 space-y-6">
        <div className="space-y-6">
          <UploadSection onImageUpload={handleImageUpload} />

          <StyleSelector
            styles={selectedStyle ? styles.filter((s) => s.category === selectedStyle.category) : styles}
            categories={categories}
            selectedStyle={selectedStyle ?? ({} as any)}
            onSelect={(style: Style) => setSelectedStyle(style)}
          />

          {selectedStyle && (
            <div className="bg-slate-800/30 border border-white/5 rounded-xl p-4">
              <h3 className="text-lg font-semibold text-purple-300 mb-2 flex items-center gap-2">📋 Выбранная прическа: {selectedStyle.name}</h3>
              <p className="text-slate-400 text-sm leading-relaxed">{selectedStyle.subtitle}</p>
            </div>
          )}

          <div className="bg-purple-950/30 border border-purple-500/20 rounded-xl p-4">
            <h3 className="text-sm font-semibold text-purple-300 mb-2 flex items-center gap-2">🚀 Как запустить Qwen Image 2.1:</h3>
            <pre className="text-xs text-slate-400 overflow-x-auto whitespace-pre-wrap font-mono bg-black/50 rounded p-3">{`# Шаг 1: Установите зависимости для Qwen Image 2.1

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers accelerate xformers

# Шаг 2: Загрузите модель Qwen2.5-VL-7B-Instruct в папку ./models

git clone https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct ./models/qwen-image-v1.5

# Шаг 3: Перезапустите backend.py — он автоматически загрузит модель

# После этого переключитесь на режим "Qwen Image 2.1" в интерфейсе`}
            </pre>
          </div>
        </div>

        <PreviewSection
          imageFile={imageFile}
          previewUrl={previewUrl}
          selectedStyle={selectedStyle}
          resultUrl={resultUrl}
          isProcessing={isProcessing}
          onApply={() => applyStyle(selectedStyle!)}
          onReset={handleReset}
          mode={generationMode}
        />
      </main>

      <footer className="border-t border-white/10 mt-8">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-slate-500 text-sm">
          ✂️ Beauty Haircut Generator — Пепельный боб • 14 причесок • Qwen Image 2.1 Ready
        </div>
      </footer>
    </div>
  );
}

export default App;