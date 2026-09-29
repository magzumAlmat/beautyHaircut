export interface Style {
  id: string;
  name: string;
  subtitle: string;
  category: 'вечерние' | 'салонные' | 'стрижки';
  desc?: string; // Краткое описание для отображения в карточке (опционально)
}

export interface File {
  name: string;
  size: number;
}

export interface QwenImageResponse {
  url?: string;
  images?: (string | Blob)[];
  [key: string]: unknown;
}