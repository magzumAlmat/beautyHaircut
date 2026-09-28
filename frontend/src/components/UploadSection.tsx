import React from 'react';
import type { File as ReactFile } from '../types';

interface Props {
  onImageLoaded: (file: ReactFile) => void;
  imageFile?: ReactFile | null;
}

export default function UploadSection({ onImageLoaded, imageFile }: Props) {
  const [isDragging, setIsDragging] = React.useState(false);

  return (
    <div className="mb-8">
      <div className="flex items-center gap-3 mb-4">
        <span className="p-2 bg-indigo-500/20 rounded-lg text-indigo-300">📷</span>
        <div>
          <h2 className="text-xl font-bold text-white">1. Загрузите фото</h2>
          <p className="text-slate-400 text-sm mt-1">Перетащите изображение сюда или кликните для выбора файла</p>
        </div>
      </div>

      {!imageFile && (
        <label
          className={`relative flex flex-col items-center justify-center p-12 rounded-3xl border-2 border-dashed transition-all cursor-pointer ${
            isDragging ? 'border-indigo-500 bg-indigo-500/10' : 'border-slate-600 hover:border-slate-500 hover:bg-white/5 bg-white/[0.02]'
          }`}
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setIsDragging(false);
            const file = Array.from(e.dataTransfer.files).find(f => f.type.startsWith('image/'));
            if (file) handleFile(file);
          }}
        >
          <input type="file" accept="image/*" className="absolute inset-0 opacity-0 cursor-pointer" onChange={(e) => {
            const file = Array.from(e.target.files).find(f => f.type.startsWith('image/'));
            if (file) handleFile(file);
          }} />

          <div className="text-center">
            <div className="mb-3 text-5xl animate-pulse-glow">📁</div>
            <p className="text-slate-200 font-medium mb-1">Перетащите фото сюда или кликните</p>
            <p className="text-slate-500 text-sm">Поддерживаются JPG, PNG (макс. 10 MB)</p>

            {imageFile?.previewUrl && (
              <div className="absolute bottom-4 left-4 right-4 flex justify-center animate-bounce-slow">
                <img src={imageFile.previewUrl!} alt="Preview" className="rounded-lg shadow-xl border border-white/10 max-h-[80px] object-contain bg-black/5" />
              </div>
            )}
          </div>
        </label>
      )}

      {imageFile && (
        <div className="flex items-center justify-between p-4 bg-white/[0.03] rounded-xl border border-white/5">
          <div className="flex items-center gap-3 flex-1 min-w-0">
            <img src={imageFile.previewUrl} alt="Selected" className="w-12 h-12 rounded-lg object-cover bg-black/40" />
            <div className="min-w-0">
              <p className="text-white text-sm font-medium truncate">{imageFile.name}</p>
              <p className="text-slate-500 text-xs">{(imageFile.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          </div>

          <button onClick={() => { onImageLoaded({ name: '', previewUrl: null, size: 0 }); }} className="text-slate-500 hover:text-red-400 transition-colors p-2 rounded-lg hover:bg-white/5">🗑️</button>
        </div>
      )}

      {imageFile && imageFile.isLoading && (
        <div className="flex items-center gap-3 p-4 bg-indigo-500/10 rounded-xl border border-indigo-500/20">
          <span className="text-xl">⏳</span>
          <p className="text-slate-300 text-sm">Обработка изображения...</p>
        </div>
      )}
    </div>
  );
}
