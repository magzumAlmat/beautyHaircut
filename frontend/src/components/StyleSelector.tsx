import React from 'react';
import type { Style } from '../types';

interface Props {
  styles: Style[];
  categories: { id: string; label: string }[];
  selectedStyle?: Style | null;
  onSelect: (style: Style) => void;
}

export default function StyleSelector({ styles, categories, selectedStyle, onSelect }: Props) {
  const [activeCategory, setActiveCategory] = React.useState('all');

  const filteredStyles = activeCategory === 'all' ? styles : styles.filter(s => s.category === activeCategory);

  return (
    <div className="mb-8">
      <div className="flex items-center gap-3 mb-4">
        <span className="p-2 bg-pink-500/20 rounded-lg text-pink-300">✂️</span>
        <div>
          <h2 className="text-xl font-bold text-white">Выберите прическу</h2>
          <p className="text-slate-400 text-sm mt-1">{categories.filter(c => c.id !== 'all').length} категории • {styles.length} стилей</p>
        </div>
      </div>

      <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
        {categories.map(cat => (
          <button key={cat.id} onClick={() => setActiveCategory(cat.id)} className={`px-4 py-2 rounded-full text-sm font-medium transition-all whitespace-nowrap ${activeCategory === cat.id ? 'bg-gradient-to-r from-pink-500 to-purple-500 text-white shadow-lg shadow-purple-500/25' : 'bg-slate-800/50 text-slate-400 hover:bg-slate-700 hover:text-slate-200 border border-white/5'}`}>
            {cat.label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
        {filteredStyles.map((style) => (
          <button key={style.id} onClick={() => onSelect(style)} className={`group relative p-4 rounded-xl text-left transition-all duration-300 border hover:border-purple-400/50 hover:shadow-lg hover:shadow-purple-900/20 ${selectedStyle?.id === style.id ? 'bg-gradient-to-br from-purple-600/40 to-pink-600/30 border-purple-500 ring-1 ring-purple-500' : 'bg-white/[0.02] border-white/5 hover:bg-white/[0.04]'}`}>
            <span className={`inline-block px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider mb-2 ${style.category === 'вечерние' ? 'bg-purple-500/30 text-purple-300 border border-purple-500/30' : style.category === 'салонные' ? 'bg-cyan-500/30 text-cyan-300 border border-cyan-500/30' : 'bg-orange-500/30 text-orange-300 border border-orange-500/30'}`}>{style.category}</span>
            <div className="mb-2">{getStyleIcon(style.id)}</div>
            <p className={`text-white font-medium text-sm line-clamp-1 transition-colors ${selectedStyle?.id === style.id ? 'text-purple-300' : ''}`}>{style.name}</p>
            <p className="text-slate-500 text-[11px] mt-0.5 line-clamp-2 leading-relaxed opacity-60 group-hover:opacity-100 transition-opacity">{style.desc}</p>

            {selectedStyle?.id === style.id && (
              <span className="absolute top-2 right-2 px-1.5 py-0.5 bg-purple-500 text-white text-[9px] font-bold rounded">✓ Выбрано</span>
            )}
          </button>
        ))}
      </div>

      {filteredStyles.length === 0 && <p className="text-slate-500 text-sm text-center py-8">Нет стилей в этой категории</p>}
    </div>
  );
}

function getStyleIcon(id: string): React.ReactNode {
  const icons: Record<string, React.ReactNode> = {
    hollywood: <span className="text-2xl">🌊</span>, high_bun: <span className="text-2xl">👑</span>, low_bun: <span className="text-2xl">🎀</span>, greek_braid: <span className="text-2xl">🧣</span>, french_twist: <span className="text-2xl">🌀</span>,
    blowout: <span className="text-2xl">💨</span>, beach_waves: <span className="text-2xl">🏖️</span>, wet_hair: <span className="text-2xl">💧</span>, high_ponytail: <span className="text-2xl">🐴</span>, straight_hair: <span className="text-2xl">⚡️</span>,
    bob: <span className="text-2xl">✂️</span>, cascade: <span className="text-2xl">🌊</span>, pixie: <span className="text-2xl">🐿️</span>, wolfcut: <span className="text-2xl">🦁</span>,
  };
  return icons[id] || <span className="text-xl">❓</span>;
}
