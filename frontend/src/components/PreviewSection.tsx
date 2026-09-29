import React from 'react';
import type { Style, File as ReactFile } from '../types';

interface Props {
  imageFile: ReactFile | null;
  previewUrl: string | null;
  resultUrl: string | null;
  isProcessing: boolean;
  selectedStyle?: Style | null;
  onApply: () => void;
  onReset: () => void;
  mode: 'qwen' | 'pillow';
}

export default function PreviewSection({ imageFile, previewUrl, resultUrl, isProcessing, selectedStyle, onApply, onReset, mode }: Props) {
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
                      <p>Генерация через Pillow...</p>
                    </div>
                  </div>
                )}

                {!isProcessing && !selectedStyle && (
                  <span className="text-slate-500 text-sm">Выберите прическу, чтобы увидеть предпросмотр</span>
                )}
              </div>
            )}
          </div>

          {resultUrl && (
            <>
              <button onClick={onReset} className="mt-3 px-6 py-2 rounded-lg bg-slate-800/50 text-slate-400 hover:text-white border border-slate-700 hover:border-purple-500/50 transition-colors text-sm font-medium">
                Сбросить
              </button>

              <div className="flex gap-3 mt-3">
                <button onClick={onApply} disabled={isProcessing} className={`flex items-center gap-2 px-6 py-2.5 rounded-lg font-medium transition-all ${
                  isProcessing ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : mode === 'qwen' 
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white shadow-lg shadow-purple-900/30'
                    : 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-900/30'
                }`}>
                  {isProcessing ? (
                    <>⏳ Генерация...</>
                  ) : (
                    <>Применить прическу</>
                  )}
                </button>

                <button onClick={onReset} className="px-6 py-2.5 rounded-lg bg-slate-800/50 text-slate-400 hover:text-white border border-slate-700 hover:border-purple-500/50 transition-colors text-sm font-medium">
                  Сбросить
                </button>
              </div>

              <p className="text-xs text-slate-500 mt-3">
                ℹ️ Режим: {mode === 'qwen' ? 'Qwen Image 2.1 (требует модели)' : 'Pillow — процедурная генерация через backend'}
              </p>
            </>
          )}
        </>
      )}
    </div>
  );
}