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
      const response = await fetch('http://localhost:8001/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: previewUrl, style_id: styleId, color: 'ash_gray' }),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setResultUrl(data.result_url);
    } catch (error) {
      console.error('Ошибка генерации:', error);
      alert('Не удалось связаться с backend сервером. Показан предпросмотр.');
    } finally {
      setIsProcessing(false);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-950 to-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-slate-900/60 border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-300 via-purple-300 to-cyan-300 bg-clip-text text-transparent">✂️ Hair Style Selector</h1>
          <a href="https://github.com/magzumAlmat/beautyHaircut" target="_blank" rel="noreferrer" className="text-xs text-slate-400 hover:text-white transition-colors flex items-center gap-1 bg-white/5 px-3 py-1.5 rounded-full border border-white/5 hover:border-purple-500/50">GitHub ↗</a>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 space-y-6">
        <UploadSection onImageLoaded={handleImageUpload} imageFile={imageFile} />

        <StyleSelector styles={styles} categories={categories} selectedStyle={selectedStyle} onSelect={(style) => { setSelectedStyle(style); setResultUrl(null); }} />

        <PreviewSection previewUrl={previewUrl} resultUrl={resultUrl} isProcessing={isProcessing} selectedStyle={selectedStyle} onApply={() => applyStyle(selectedStyle?.id || '')} onReset={() => { setResultUrl(null); setSelectedStyle(null); }} />
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 mt-12 py-6 text-center text-slate-500 text-sm">
        <p>Поддерживает {styles.length} причесок • Интеграция с Qwen Image 2.1</p>
        <p className="text-xs mt-1 opacity-60">Backend API: http://localhost:8001 | Frontend: http://localhost:3000</p>
      </footer>
    </div>
  );
}

export default App;
