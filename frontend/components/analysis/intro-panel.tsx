"use client";
import { useState } from "react";
import { toast } from "sonner";

interface Props {
  zh: string;
  en: string;
}

export function IntroPanel({ zh, en }: Props) {
  const [lang, setLang] = useState<"zh" | "en">("zh");
  const text = lang === "zh" ? zh : en;

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text);
    toast.success("已复制到剪贴板");
  };

  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        {(["zh", "en"] as const).map((l) => (
          <button
            key={l}
            onClick={() => setLang(l)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              lang === l
                ? "bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900"
                : "bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700"
            }`}
          >
            {l === "zh" ? "中文" : "English"}
          </button>
        ))}
      </div>

      <div className="relative rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 p-4">
        <p className="text-sm leading-relaxed text-zinc-700 dark:text-zinc-300 whitespace-pre-wrap">{text}</p>
        <button
          onClick={handleCopy}
          className="absolute top-3 right-3 text-xs text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded px-2 py-1 transition-colors"
        >
          复制
        </button>
      </div>
    </div>
  );
}
