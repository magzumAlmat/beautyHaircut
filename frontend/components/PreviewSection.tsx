interface PreviewProps {
  imageFile?: { name: string; size: number };
  previewUrl?: string | null;
  resultUrl?: string | null;
  selectedStyle?: { id: string; name: string } | null;
  isProcessing: boolean;
}

export default function PreviewSection({ imageFile, previewUrl, resultUrl, selectedStyle, isProcessing }: PreviewProps) {
  if (!previewUrl || !selectedStyle) return null;

  return (
    <div className="w-full max-w-2xl mx-auto p-4 space-y-3">
      {/* Original preview */}
      <div className="rounded-xl overflow-hidden border border-slate-700 bg-slate-900/50">
        <div className="text-xs text-slate-500 px-2 py-1 bg-slate-800/50 rounded-t">Оригинал</div>
        <img src={previewUrl} alt="Original" className="w-full max-h-40 object-cover" />
      </div>

      {/* Result */}
      <div className={`rounded-xl overflow-hidden border bg-slate-900/50 transition-all ${resultUrl ? 'border-green-500 ring-2 ring-green-500/30' : 'border-slate-700'}`}>
        <div className="px-2 py-1 bg-slate-800/50 rounded-t flex items-center gap-2 text-xs">
          {resultUrl ? (
            <>✅ Результат</>
          ) : selectedStyle && !resultUrl && !isProcessing && (
            <>⏳ Генерация...</>
          )}
        </div>

        {!resultUrl && isProcessing && (
          <div className="w-full h-40 flex items-center justify-center">
            <span className="text-slate-500 text-sm animate-pulse">Генерируем прическу...</span>
          </div>
        )}

        {resultUrl && (
          <>
            <img src={resultUrl} alt={`Haircut: ${selectedStyle.name}`} className="w-full max-h-48 object-contain" />
            <div className="p-2 bg-slate-900/80 border-t flex items-center justify-between">
              <span className="text-xs text-slate-400">Сгенерировано через Pillow fallback</span>
              <button
                onClick={() => window.open(resultUrl, '_blank')}
                className="px-3 py-1 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-xs font-medium transition-colors"
              >
                Открыть в новой вкладке ↗
              </button>
            </div>
          </>
        )}

        {!resultUrl && !isProcessing && selectedStyle && (
          <div className="w-full h-40 flex items-center justify-center">
            <span className="text-slate-500 text-sm">Результат появится здесь</span>
          </div>
        )}
      </div>

      {/* Action buttons */}
      {resultUrl && (
        <div className="flex gap-2">
          <button
            onClick={() => window.open(resultUrl, '_blank')}
            className="flex-1 px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg font-medium transition-colors"
          >
            Открыть результат ↗
          </button>
        </div>
      )}
    </div>
  );
}