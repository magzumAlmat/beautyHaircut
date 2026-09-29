import React, { useRef } from 'react';

export default function UploadSection({ onImageUpload }: { onImageUpload: (file: File) => void }) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Обработка drag&drop
  function handleDragOver(event: React.DragEvent<HTMLDivElement>): void {
    event.preventDefault();
    event.stopPropagation();
  }

  function handleDrop(event: React.DragEvent<HTMLDivElement>): void {
    event.preventDefault();
    event.stopPropagation();

    const file = event.dataTransfer.files[0];
    
    // Если перетащили файл — используем его
    if (file && file.type.startsWith('image/')) {
      onImageUpload(file);
      return;
    }

    // Иначе открываем диалог выбора файла
    fileInputRef.current?.click();
  }

  // Обработка клика по зоне
  function handleClick(event: React.MouseEvent<HTMLDivElement>): void {
    event.stopPropagation();
    fileInputRef.current?.click();
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
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className="border-2 border-dashed border-slate-600 rounded-xl p-8 text-center cursor-pointer hover:border-pink-500 hover:bg-pink-500/5 transition-all duration-300 group"
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file && file.type.startsWith('image/')) {
              onImageUpload(file);
            }
            // Очищаем input чтобы можно было выбрать тот же файл повторно
            e.target.value = '';
          }}
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