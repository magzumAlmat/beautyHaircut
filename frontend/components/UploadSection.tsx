import type { ReactNode } from 'react';

interface UploadProps {
  children: ReactNode;
}

export default function UploadSection({ children }: UploadProps) {
  return <div className="w-full">{children}</div>;
}