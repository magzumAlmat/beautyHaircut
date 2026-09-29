export interface Style {
  id: string;
  name: string;
  subtitle: string;
  category: 'вечерние' | 'салонные' | 'стрижки';
}

export interface File {
  name: string;
  size: number;
}