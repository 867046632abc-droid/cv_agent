"use client";
import { useRef } from "react";
import { cn } from "@/lib/utils";

interface Props {
  file: File | null;
  onChange: (file: File) => void;
  error?: string;
}

export function ResumeDropzone({ file, onChange, error }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const dropped = e.dataTransfer.files[0];
    if (dropped) onChange(dropped);
  };

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      onClick={() => inputRef.current?.click()}
      className={cn(
        "border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors",
        error
          ? "border-red-400 bg-red-50 dark:bg-red-950"
          : file
          ? "border-emerald-400 bg-emerald-50 dark:bg-emerald-950"
          : "border-zinc-300 hover:border-zinc-400 dark:border-zinc-700"
      )}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        className="hidden"
        onChange={(e) => { if (e.target.files?.[0]) onChange(e.target.files[0]); }}
      />
      {file ? (
        <div className="space-y-1">
          <p className="font-medium text-emerald-700 dark:text-emerald-400">{file.name}</p>
          <p className="text-sm text-zinc-500">{(file.size / 1024).toFixed(1)} KB</p>
        </div>
      ) : (
        <div className="space-y-2">
          <p className="text-zinc-600 dark:text-zinc-400">拖拽 PDF 到此处，或点击上传</p>
          <p className="text-xs text-zinc-400">仅支持 PDF，最大 10 MB</p>
        </div>
      )}
      {error && <p className="mt-2 text-sm text-red-500">{error}</p>}
    </div>
  );
}
