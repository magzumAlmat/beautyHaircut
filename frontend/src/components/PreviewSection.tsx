import React from 'react';
import type { Style, File as ReactFile } from '../types';

interface Props {
  previewUrl: string | null;
  resultUrl: string | null;
  isProcessing: boolean;
  selectedStyle?: { id: string; name: string } | null;
  onApply: () => void;
  onReset: () => void;
  mode: 'qwen' | 'pillow';
}

export default function PreviewSection({ previewUrl, resultUrl, isProcessing, selectedStyle, onApply, onReset, mode }: Props) {
  return (
    <div className="mb-12">
      <div className="flex items-center gap-3 mb-4">
        <span className={`p-2 rounded-lg transition-all ${mode === 'qwen' ? 'bg-purple-500/20 text-purple-300' : 'bg-blue-500/20 text-blue-300'}`}>
          {mode === 'qwen' ? '🤖 Qwen Image 2.1' : '🖼️ Pillow Fallback'}
        </span>
        <div>
          <h2 className="text-xl font-bold text-white">Предпросмотр результата</h2>
          <p className="text-slate-400 text-sm mt-1">Нажмите «Применить», чтобы сгенерировать изображение</p>
        </div>
      </div>

      {!previewUrl ? (
        <div className="flex flex-col items-center justify-center p-12 bg-white/[0.02] rounded-3xl border border-dashed border-slate-700 text-center">
          <span className="text-6xl mb-3 opacity-50">🖼️</span>
          <p className="text-slate-400 text-sm">Загрузите фото, чтобы увидеть предпросмотр</p>
        </div>
      ) : (
        <>
          {!resultUrl && (
            <div className="mb-3 flex items-center justify-between px-1">
              <span className="text-slate-500 text-xs font-medium uppercase tracking-wider">Исходное изображение</span>
              {selectedStyle && <span className="px-2 py-1 rounded bg-purple-500/20 text-purple-300 text-xs border border-purple-500/30">Подготовлено для: {selectedStyle.name}</span>}
            </div>
          )}

          <div className={`relative rounded-2xl overflow-hidden shadow-2xl transition-all duration-700 ${resultUrl ? 'ring-2 ring-purple-500' : 'border border-slate-700'}`}>
            {resultUrl && (
              <img src={resultUrl} alt="Result" className="w-full h-auto max-h-[60vh] object-contain bg-black/80" />
            )}

            {!resultUrl && previewUrl && (
              <div className={`flex flex-col items-center justify-center h-[350px] bg-slate-900 ${selectedStyle ? 'overflow-hidden' : ''}`}>
                {selectedStyle && (
                  <div className="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm">
                    <span className="text-white font-medium text-lg backdrop-blur-sm px-6 py-3 rounded-xl border border-white/20 bg-black/50">{selectedStyle.name}</span>
                  </div>
                )}

                {isProcessing && (
                  <div className="absolute inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center">
                    <div className="text-center text-white">
                      <span className="text-5xl mb-3 animate-pulse">⏳</span>
                      <p className="font-medium">Генерация прически...</p>
                    </div>
                  </div>
                )}

                {!selectedStyle && !isProcessing && (
                  <img src={previewUrl} alt="Original" className="max-w-full max-h-[60vh] object-contain" />
                )}
              </div>
            )}
          </div>

          {!resultUrl && (
            <div className="flex gap-3 mt-4 justify-center">
              <button onClick={onApply} disabled={!selectedStyle || isProcessing} className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all duration-300 ${!selectedStyle || isProcessing ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-400 hover:to-purple-500 text-white shadow-lg shadow-purple-900/30 hover:shadow-xl hover:shadow-purple-700/50 transform hover:-translate-y-0.5'}`}>
                {isProcessing ? <>⏳ Генерируем...</> : selectedStyle ? <>✨ Применить {selectedStyle.name}</> : <span>Выберите прическу</span>}
              </button>

              <button onClick={onReset} className="px-6 py-3 rounded-xl bg-slate-800/50 text-slate-400 hover:bg-red-500/20 hover:text-red-300 hover:border-red-500/50 border border-white/5 transition-all duration-300">Сбросить</button>
            </div>
          )}

          {resultUrl && (
            <div className="mt-4 flex gap-3 items-center justify-between px-6 py-3 bg-green-500/10 border border-green-500/20 rounded-xl">
              <span className="text-green-300 text-sm font-medium flex items-center gap-2">✅ Результат сгенерирован!</span>
              <button onClick={onReset} className="px-4 py-1.5 rounded-lg bg-slate-700/50 hover:bg-red-500/20 hover:text-red-300 text-slate-300 text-xs transition-all">Сбросить</button>
            </div>
          )}

          {resultUrl && (
            <div className="mt-4 flex items-center justify-between px-6 py-3 bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-green-500/20 rounded-xl">
              <span className="text-green-300 text-sm font-medium flex items-center gap-2">
                📥 Скачать результат
              </span>
              <a href={resultUrl} download={`haircut-${selectedStyle?.id || 'unknown'}.png`} className="px-4 py-1.5 rounded-lg bg-green-600/80 hover:bg-green-500 text-white text-xs font-medium transition-all flex items-center gap-1">
                ⬇️ Скачать
              </a>
            </div>
          )}
        </>
      )}

      <p className="text-slate-600 text-xs mt-4 text-center">Сервис использует алгоритмы процедурной генерации причесок. Результаты могут отличаться от реальных фото.</p>
    </div>
  );
}