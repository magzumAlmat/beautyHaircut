import React from 'react';

export default function UploadSection({ onImageUpload }: { onImageUpload: (file: File) => void }) {
  const fileInputRef = React.useRef<HTMLInputElement>(null);

  function handleFileSelect(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    onImageUpload(file);
  }

  return (
    <div className="mb-6">
      <div className="flex items-center gap-3 mb-4">
        <span className="p-2 bg-pink-500/20 rounded-lg text-pink-300">📤</span>
        <div>
          <h2 className="text-xl font-bold text-white">Загрузить фото</h2>
          <p className="text-slate-400 text-sm mt-1">Перетащите изображение или нажмите для выбора файла</p>
        </div>
      </div>

      <div
        onDragOver={(e) => { e.preventDefault(); }}
        onDrop={(event) => {
          const file = event.dataTransfer.files[0];
          if (!file || !file.type.startsWith('image/')) return;
          onImageUpload(file);
        }}
        className="border-2 border-dashed border-slate-600 rounded-xl p-8 text-center cursor-pointer hover:border-pink-500 hover:bg-pink-500/5 transition-all duration-300 group"
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={handleFileSelect}
        />

        <div className="flex flex-col items-center gap-2">
          <span className="text-5xl group-hover:scale-110 transition-transform duration-300">📁</span>
          <p className="text-slate-400 font-medium">Перетащите фото сюда или кликните для выбора</p>
          <p className="text-slate-600 text-xs mt-1">Поддерживаются: JPG, PNG, WebP (макс. 10 MB)</p>
        </div>
      </div>
    </div>
  );
}