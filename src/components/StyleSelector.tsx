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
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 12c-1.197-.983-2.223-2.258-3-3.707V14h1v-5m0 11h-4l-6-4 6-4v3" /></svg>;
    case 'bun':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 10c2-2 6-2 8 0s2 6 0 8-6 2-8 0-2-6zM4 12a8 8 0 0116 0m-3 0c0 2.5-2 4.5-4 4.5S7 14.5 7 12" /></svg>;
    case 'bun_low':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 16c-1-2-2-5-3-7h6s-2 2-3 7m2-8a3 3 0 013 3v2a1 1 0 00-2 0V9.414l-3-3" /></svg>;
    case 'braid':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 7c-2.21 0-4 1.79-4 4s1.79 4 4 4m6 0c2.21 0 4-1.79 4-4s-1.79-4-4-4m-3 8a3 3 0 100-6 3 3 0 000 6zM5 9h14M5 15h14" /></svg>;
    case 'shell':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6c-2.954 0-5.678.843-7.71 2.25a1 1 0 00-.126 1.66l1.26 1.13a1 1 0 001.19.07L10 15v3h4v-3l2.38-2.08a1 1 0 001.19-.07l1.26-1.13a1 1 0 00-.126-1.66C17.678 6.843 14.954 6 12 6z" /></svg>;
    case 'volume':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" /></svg>;
    case 'waves_loose':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 8c1.5-2 5-2 6.5 0s3.5 4.5 5 4.5a4.5 4.5 0 00-5-4.5m-9 5c-1.5 2-.5 6 2 7s4-2 4-6" /></svg>;
    case 'gel':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 8h10a3 3 0 013 3v6a3 3 0 01-3 3H7a3 3 0 01-3-3v-6a3 3 0 013-3z" /></svg>;
    case 'pony':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M18 9a3 3 0 00-3-3 6 6 0 00-6 6 6 6 0 004 5.77l2-2m-4 2l-4 2" /></svg>;
    case 'straight':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M6 8l-4 4m4-4l4 4m-4 4l4-4m4 0V3" /></svg>;
    case 'bob':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M6 8c2-2 6-2 8 0s3 4 3 7a3 3 0 01-3 3H9a3 3 0 01-3-3c0-3 1-6 3-7z" /></svg>;
    case 'layers':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 6h16M4 10h16M4 14h10m-11 6v-3m9 3v-3" /></svg>;
    case 'short':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 6h8a3 3 0 013 3v3m-8 4c2.5 0 4.5-1.5 4.5-4V9H7a3 3 0 00-3 3v3" /></svg>;
    case 'shaggy':
      return <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={iconClass}><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.813 15.904l-6.778 5.21a2 2 0 00.724 3.436l1.413.909a2 2 0 002.81-.507l3.356-4.14a2 2 0 00-.314-2.65zM15.29 13.56c.81-.634 1.862-.623 2.607.02l.71.68a2 2 0 001.62.6h.135l-5.935 3.145c-1.262.686-2.797-.092-3.14-1.462l-.184-.56z" /></svg>;
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
