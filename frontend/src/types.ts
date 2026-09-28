export interface Style {
  id: string;
  name: string;
  desc: string;
  category: 'вечерние' | 'салонные' | 'стрижки';
}

export interface File {
  name: string;
  previewUrl: string | null;
  size: number;
  isLoading?: boolean;
}
