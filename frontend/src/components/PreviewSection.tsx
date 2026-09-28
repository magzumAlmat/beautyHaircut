import React from 'react';

interface PreviewSectionProps {
  previewUrl: string | null;
  resultUrl: string | null;
  isProcessing: boolean;
  selectedStyle: any | null;
  onApply: () => void;
  onReset: () => void;
}

export default function PreviewSection({
  previewUrl,
  resultUrl,
  isProcessing,
  selectedStyle,
  onApply,
  onReset,
}: PreviewSectionProps) {
  return (
    <section className="space-y-4">
      <div>
        <h2 className="text-xl font-semibold text-white mb-1 flex items-center gap-2">
          👁️ Предпросмотр
          <span className="text-slate-500 text-sm font-normal ml-auto">
            {selectedStyle ? selectedStyle.name : '—'}
          </span>
        </h2>
      </div>

      {/* Preview Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 items-start">

        {/* Original Image */}
        {previewUrl && (
          <div className="relative group rounded-xl overflow-hidden border border-white/20 bg-slate-800/50">
            <img src={previewUrl} alt="Original" className="w-full aspect-[3/4] object-cover" />
            <div className="absolute inset-x-0 bottom-0 p-3 bg-gradient-to-t from-black/90 via-transparent to-transparent">
              <span className="text-slate-300 text-sm font-medium flex items-center gap-2">
                📷 Оригинал
              </span>
            </div>
          </div>
        )}

        {/* Result (with placeholder) */}
        {isProcessing ? (
          <div className="relative rounded-xl overflow-hidden border border-white/20 bg-slate-800/50">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center space-y-3 p-6">
                <div className="w-12 h-12 mx-auto relative">
                  <svg viewBox="0 0 48 48" fill="none" className="animate-spin text-pink-400 w-12 h-12">
                    <circle cx="24" cy="24" r="20" stroke="currentColor" strokeWidth="3" strokeDasharray="6 4" />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center text-sm font-medium text-white">
                    ✨
                  </div>
                </div>
                <p className="text-slate-300 text-sm">
                  Генерирую прическу…
                </p>
                {selectedStyle && (
                  <p className="text-slate-500 text-xs">{selectedStyle.name}</p>
                )}
              </div>
            </div>
          </div>
        ) : resultUrl ? (
          <div className="relative rounded-xl overflow-hidden border border-emerald-400/50 bg-slate-800/50 shadow-lg shadow-emerald-900/20">
            <img src={resultUrl} alt="Result" className="w-full aspect-[3/4] object-cover" />
            <div className="absolute inset-x-0 bottom-0 p-3 bg-gradient-to-t from-black/90 via-transparent to-transparent">
              <span className="text-emerald-300 text-sm font-medium flex items-center gap-2">
                🎉 Результат! Скачать
              </span>
            </div>
            <a
              href={resultUrl}
              download={`hair-style-${selectedStyle?.id || 'unknown'}.png`}
              className="absolute inset-x-0 top-3 p-2 bg-black/60 backdrop-blur-sm text-white text-xs font-medium rounded-lg opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-1"
            >
              ⬇️ Скачать PNG
            </a>
          </div>
        ) : (
          <div className="rounded-xl border border-white/20 bg-slate-800/30 p-6 text-center">
            <div className="mx-auto w-12 h-12 rounded-full bg-slate-700/50 flex items-center justify-center mb-3 text-2xl">
              🎨
            </div>
            <p className="text-slate-400 text-sm">
              Выбери прическу, чтобы увидеть результат
            </p>
          </div>
        )}

      </div>

      {/* Action Buttons */}
      <div className="flex gap-3 pt-2">
        {!selectedStyle ? (
          <button
            onClick={onReset}
            disabled={!previewUrl}
            className={`px-6 py-3 rounded-xl font-medium transition-all ${
              previewUrl
                ? 'bg-slate-700/50 text-white hover:bg-slate-600 border border-white/10'
                : 'bg-slate-800 text-slate-500 cursor-not-allowed opacity-50'
            }`}
          >
            Сбросить
          </button>
        ) : (
          <>
            <button
              onClick={onApply}
              disabled={isProcessing}
              className="flex-1 px-6 py-3 rounded-xl font-medium bg-gradient-to-r from-pink-500 to-purple-600 text-white hover:from-pink-400 hover:to-purple-500 active:scale-[0.98] transition-all disabled:opacity-50 disabled:pointer-events-none flex items-center justify-center gap-2 shadow-lg shadow-pink-500/25"
            >
              {isProcessing ? (
                <>
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                  Генерирую…
                </>
              ) : (
                <>🎨 Применить прическу</>
              )}
            </button>

            <button
              onClick={onReset}
              className="px-6 py-3 rounded-xl font-medium bg-slate-700/50 text-white hover:bg-slate-600 border border-white/10 transition-all"
            >
              Отмена
            </button>
          </>
        )}
      </div>

      {/* Instructions */}
      <div className="bg-slate-800/30 rounded-xl p-4 text-sm text-slate-400 border border-white/10">
        <p className="flex items-start gap-2">
          <span className="text-pink-400 font-bold mt-0.5">💡 Совет:</span>
          Для лучшего результата загружайте фото с чётким изображением лица и волос. Избегайте очень тёмных или сильно контрастных фонов.
        </p>
      </div>
    </section>
  );
}
