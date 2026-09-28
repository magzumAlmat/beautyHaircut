import React, { useRef } from 'react';

interface UploadSectionProps {
  onImageLoaded: (file: File) => void;
}

export default function UploadSection({ onImageLoaded }: UploadSectionProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  return (
    <section className="space-y-4">
      <div>
        <h2 className="text-xl font-semibold text-white mb-1 flex items-center gap-2">
          📁 Загрузите фото
          <span className="text-slate-500 text-sm font-normal ml-auto">JPG, PNG, WEBP</span>
        </h2>
      </div>

      <label
        htmlFor="image-upload"
        className={`group relative flex items-center justify-center gap-3 w-full max-w-md mx-auto h-48 rounded-2xl border-2 border-dashed transition-all cursor-pointer overflow-hidden ${
          props.imageFile ? 'border-emerald-500/50 bg-emerald-500/10' : 'border-white/30 hover:border-pink-400/60 hover:bg-white/5'
        }`}
      >
        <input
          id="image-upload"
          type="file"
          ref={fileInputRef}
          accept="image/*"
          className="absolute inset-0 opacity-0 cursor-pointer"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file && !props.imageFile) onImageLoaded(file);
            else fileInputRef.current!.value = '';
          }}
        />

        <div className="text-center pointer-events-none">
          <span
            className={`inline-block p-3 rounded-full mb-2 text-xl transition-all ${
              props.imageFile ? 'bg-emerald-500/20 text-emerald-300' : 'bg-white/10 group-hover:bg-pink-400/20'
            }`}
          >
            {props.imageFile ? (
              <span aria-hidden="true">✓</span>
            ) : (
              <>📸 <span className="text-xs align-top ml-1">(кликните или перетащите)</span></>
            )}
          </span>

          <p className="text-slate-300 font-medium">
            {props.imageFile ? (
              <>✓ {props.imageFile.name.length > 25 ? props.imageFile.name.slice(0, 22) + '...' : props.imageFile.name}</>
            ) : (
              'Перетащите фото сюда или кликните для выбора'
            )}
          </p>

          <p className="text-slate-500 text-xs mt-1">Максимум 10 MB</p>
        </div>
      </label>

      {/* Image Preview */}
      {props.imageFile && (
        <div
          onClick={() => fileInputRef.current?.click()}
          className="relative w-full max-w-md mx-auto rounded-xl overflow-hidden cursor-pointer group"
        >
          <img
            src={URL.createObjectURL(props.imageFile)}
            alt="Preview"
            className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
          />
          <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
            <span className="text-white font-medium">🔄 Заменить фото</span>
          </div>
        </div>
      )}

      {/* Error state */}
      {props.imageFile && props.imageFile.size > 10 * 1024 * 1024 && (
        <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-sm text-red-300">
          ⚠️ Файл слишком большой. Максимум 10 MB
        </div>
      )}

      {/* Подсказка, если не выбрано фото */}
      {!props.imageFile && (
        <p className="text-slate-500 text-sm italic pl-2">
          Пока что ни одного фото не загружено...
        </p>
      )}
    </section>
  );
}

// --- Props interface for TypeScript type checking ---
interface UploadSectionProps {
  onImageLoaded: (file: File) => void;
  imageFile?: File | null; // ← теперь это prop, а не глобальная переменная
}
