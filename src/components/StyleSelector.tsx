import React, { useState } from 'react';

interface Style {
  id: string;
  name: string;
  subtitle: string;
  category: 'вечерние' | 'салонные' | 'стрижки';
  icon: string;
}

interface Categories {
  id: string;
  label: string;
}

interface StyleSelectorProps {
  styles: Style[];
  categories: Categories[];
  selectedStyle: Style | null;
  onSelect: (style: Style) => void;
}

function getIcon(iconName: string, className?: string): JSX.Element {
  const iconClass = `w-6 h-6 ${className ?? ''}`;

  switch (iconName) {
    case 'waves':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 12 c-1.197 -0.983 -2.223 -2.258 -3 -3.707 V14 h1 v-5 m0 11 h-4 l-6 -4 6 -4 v3" /></svg>;
    case 'bun':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 10c2 -2 6 -2 8 0s2 6 0 8 -6 2 -8 0 -2 -6z M4 12a8 8 0 0 1 16 0m-3 0c0 2.5 -2 4.5 -4 4.5S7 14.5 7 12" /></svg>;
    case 'bun_low':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 16 c-1 -2 -2 -5 -3 -7 h6 s-2 2 -3 7 m2 -8 a3 3 0 0 1 3 3 v2 a1 1 0 0 0 -2 0 V9.414 l-3 -3" /></svg>;
    case 'braid':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 7 c-2.21 0 -4 1.79 -4 4 s1.79 4 4 4 m6 0 c2.21 0 4 -1.79 4 -4 s-1.79 -4 -4 -4 m-3 8 a3 3 0 1 0 0 -6 a3 3 0 0 0 0 6 z M5 9 h14 M5 15 h14" /></svg>;
    case 'shell':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6 c-2.954 0 -5.678 0.843 -7.71 2.25 a1 1 0 0 0 -0.126 1.66 l1.26 1.13 a1 1 0 0 0 1.19 0.07 L10 15 v3 h4 v-3 l2.38 -2.08 a1 1 0 0 0 1.19 -0.07 l1.26 -1.13 a1 1 0 0 0 -0.126 -1.66 C17.678 6.843 14.954 6 12 6 z" /></svg>;
    case 'volume':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16 V4 m0 0 L3 8 m4 -4 l4 4 m6 0 v12 m0 0 l4 -4 m-4 4 l-4 -4" /></svg>;
    case 'waves_loose':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 8 c1.5 -2 5 -2 6.5 0 s3.5 4.5 5 4.5 a4.5 4.5 0 0 0 -5 -4.5 m-9 5 c-1.5 2 -0.5 6 2 7 s4 -2 4 -6" /></svg>;
    case 'gel':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 8 h10 a3 3 0 0 1 3 3 v6 a3 3 0 0 1 -3 3 H7 a3 3 0 0 1 -3 -3 v-6 a3 3 0 0 1 3 -3 z" /></svg>;
    case 'pony':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M18 9 a3 3 0 0 0 -3 -3 a6 6 0 0 0 -6 6 a6 6 0 0 0 4 5.77 l2 -2 m-4 2 l-4 2" /></svg>;
    case 'straight':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M6 8 l-4 4 m4 -4 l4 4 m-4 4 l-4 -4 m4 0 V3" /></svg>;
    case 'bob':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M6 8 c2 -2 6 -2 8 0 s3 4 3 7 a3 3 0 0 1 -3 3 H9 a3 3 0 0 1 -3 -3 c0 -3 1 -6 3 -7 z" /></svg>;
    case 'layers':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 6 h16 M4 10 h16 M4 14 h10 m-11 6 v-3 m9 3 v-3" /></svg>;
    case 'short':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 6 h8 a3 3 0 0 1 3 3 v3 m-8 4 c2.5 0 4.5 -1.5 4.5 -4 V9 H7 a3 3 0 0 0 -3 3 v3" /></svg>;
    case 'shaggy':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.813 15.904 l-6.778 5.21 a2 2 0 0 0 0.724 3.436 l1.413 0.909 a2 2 0 0 0 2.81 -0.507 l3.356 -4.14 a2 2 0 0 0 -0.314 -2.65 z M15.29 13.56 c0.81 -0.634 1.862 -0.623 2.607 0.02 l0.71 0.68 a2 2 0 0 0 1.62 0.6 h0.135 l-5.935 3.145 c-1.262 0.686 -2.797 -0.092 -3.14 -1.462 l-0.184 -0.56 z" /></svg>;
    default:
      return <span className="text-xl">❓</span>;
  }
}

export default function StyleSelector({ styles, categories, selectedStyle, onSelect }: StyleSelectorProps) {
  const [activeCategory, setActiveCategory] = useState<string>('all');

  const filteredStyles = activeCategory === 'all'
    ? styles
    : styles.filter((s) => s.category === activeCategory);

  return (
    <section className="space-y-4">
      <div>
        <h2 className="text-xl font-semibold text-white mb-1 flex items-center gap-2">
          ✂️ Выбери прическу
          <span className="text-slate-500 text-sm font-normal ml-auto">
            {filteredStyles.length} вариантов
          </span>
        </h2>
      </div>

      {/* Category Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setActiveCategory(cat.id)}
            className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all ${
              activeCategory === cat.id
                ? 'bg-gradient-to-r from-pink-500 to-purple-500 text-white shadow-lg shadow-pink-500/25'
                : 'bg-slate-800/50 text-slate-400 hover:bg-slate-700/50 hover:text-white border border-white/10'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Styles Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
        {filteredStyles.map((style) => (
          <button
            key={style.id}
            onClick={() => onSelect(style)}
            className={`group relative rounded-xl p-4 text-left transition-all duration-200 border ${
              selectedStyle?.id === style.id
                ? 'bg-gradient-to-br from-pink-500/20 to-purple-500/20 border-pink-400/50 shadow-lg shadow-pink-500/10'
                : 'bg-slate-800/30 border-white/10 hover:border-pink-400/40 hover:bg-slate-700/50'
            }`}
          >
            <div className="flex items-start justify-between gap-2">
              <span
                className={`text-xl transition-transform duration-300 ${
                  selectedStyle?.id === style.id ? 'scale-110' : ''
                }`}
              >
                {getIcon(style.icon)}
              </span>
              {/* Selected badge */}
              {selectedStyle?.id === style.id && (
                <div className="absolute -top-2 -right-2 bg-gradient-to-r from-pink-500 to-purple-500 text-white text-xs font-bold px-2 py-1 rounded-full shadow-lg">
                  ✓
                </div>
              )}
            </div>

            <h3 className="text-slate-200 font-medium mt-1 group-hover:text-pink-300 transition-colors truncate">
              {style.name}
            </h3>

            <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed pt-1">
              {style.subtitle}
            </p>

            {/* Category badge */}
            <span className={`absolute bottom-2 right-2 text-[10px] uppercase tracking-wider font-semibold px-2 py-0.5 rounded-full bg-slate-900/60 border border-white/5 ${
              style.category === 'вечерние' ? 'text-pink-400' :
              style.category === 'салонные' ? 'text-cyan-400' :
              'text-emerald-400'
            }`}>
              {style.category}
            </span>
          </button>
        ))}

        {/* Empty state */}
        {filteredStyles.length === 0 && (
          <div className="col-span-full py-12 text-center">
            <p className="text-slate-500">Нет причесок в категории "{categories.find(c => c.id === activeCategory)?.label}"</p>
          </div>
        )}
      </div>
    </section>
  );
}
