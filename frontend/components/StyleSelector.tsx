import type { Style } from '../types';

interface StyleSelectorProps {
  selected: Style | null;
  onSelect: (style: Style) => void;
}

const styles: Style[] = [
  { id: 'hollywood_waves', name: 'Голливудские волны', subtitle: 'Гладкие, крупные, идеально синхронные локоны на одну сторону', category: 'вечерние' },
  { id: 'high_bun', name: 'Высокий текстурный пучок', subtitle: 'Элегантная собранная прическа с объемом у корней и легкими прядями у лица', category: 'вечерние' },
  { id: 'low_bun', name: 'Низкий гладкий пучок', subtitle: 'Строгий, минималистичный вариант, создающий лаконичный образ', category: 'вечерние' },
  { id: 'greek_braid', name: 'Греческая коса', subtitle: 'Пышное объемное плетение, плавно переходящее в хвост', category: 'вечерние' },
  { id: 'french_twist', name: 'Французский твист (ракушка)', subtitle: 'Классический вертикальный валик на затылке', category: 'вечерние' },
  { id: 'brush_volume', name: 'Брашинг-объем', subtitle: 'Пышная укладка феном и круглой щеткой', category: 'салонные' },
  { id: 'beach_waves', name: 'Пляжные волны (Beach Waves)', subtitle: 'Расслабленные, слегка небрежные текстурные локоны', category: 'салонные' },
  { id: 'wet_hair', name: 'Эффект «влажных волос»', subtitle: 'Трендовая подиумная укладка с помощью геля', category: 'салонные' },
  { id: 'high_textured_ponytail', name: 'Высокий текстурный хвост', subtitle: 'Объемный хвост с начесом или легкой завивкой', category: 'салонные' },
  { id: 'pearl_bun', name: 'Пудровый пучок (Pearl Bun)', subtitle: 'Нежный пучок на макушке с мягкими, слегка небрежными прядями по бокам — элегантный вариант для офиса или свидания', category: 'салонные' },
  { id: 'bob', name: 'Каре / Боб-каре', subtitle: 'Классическое каре, боб-каре или с удлинением', category: 'стрижки' },
  { id: 'cascade', name: 'Каскад и Лесенка', subtitle: 'Многоступенчатые стрижки для объема на средние и длинные волосы', category: 'стрижки' },
  { id: 'pixie', name: 'Пикси', subtitle: 'Короткая, динамичная стрижка с рваными прядями', category: 'стрижки' },
  { id: 'wolfcut', name: 'Вулфкат (Wolfcut) / Шегги', subtitle: 'Текстурные, намеренно растрепанные многослойные стрижки', category: 'стрижки' },
];

const categories = [
  { id: 'all', label: 'Все' },
  { id: 'вечерние', label: 'Вечерние и торжественные' },
  { id: 'салонные', label: 'Салонные укладки' },
  { id: 'стрижки', label: 'Трендовые стрижки' },
];

export default function StyleSelector({ selected, onSelect }: StyleSelectorProps) {
  const [categoryFilter, setCategoryFilter] = useState<'all' | 'вечерние' | 'салонные' | 'стрижки'>('all');

  return (
    <div className="w-full max-w-2xl mx-auto p-6 space-y-4">
      <h2 className="text-xl font-bold text-white mb-3 flex items-center gap-2">
        ✂️ Выберите прическу:
      </h2>

      {/* Category tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {categories.map(cat => (
          <button
            key={cat.id}
            onClick={() => setCategoryFilter(cat.id)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              categoryFilter === cat.id
                ? 'bg-pink-500 text-white'
                : 'bg-slate-800/50 text-slate-300 hover:bg-slate-700/50'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Grid of styles */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {styles.filter(s => categoryFilter === 'all' || s.category === categoryFilter).map(style => (
          <button
            key={style.id}
            onClick={() => onSelect(style)}
            className={`p-4 rounded-xl border text-left transition-all ${
              selected?.id === style.id
                ? 'border-pink-500 bg-pink-500/10 ring-2 ring-pink-500/30'
                : 'border-slate-700 bg-slate-800/40 hover:border-purple-500 hover:bg-slate-700/60'
            }`}
          >
            <div className="font-semibold text-white mb-1">{style.name}</div>
            <div className="text-xs text-slate-400 line-clamp-2">{style.subtitle}</div>
          </button>
        ))}
      </div>
    </div>
  );
}

function useState<T>(initial: T): [T, (val: T | ((prev: T) => T)) => void] {
  return [initial as any];
}