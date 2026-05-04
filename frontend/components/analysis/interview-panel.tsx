"use client";
import { useState } from "react";
import type { InterviewQuestions } from "@/lib/types";

const CATEGORIES = [
  { key: "technical" as const, label: "技术深挖" },
  { key: "project" as const, label: "项目经历" },
  { key: "gap" as const, label: "Gap 应对" },
];

export function InterviewPanel({ questions }: { questions: InterviewQuestions }) {
  const [openIdx, setOpenIdx] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      {CATEGORIES.map(({ key, label }) => (
        <div key={key}>
          <h3 className="font-semibold text-zinc-800 dark:text-zinc-200 mb-3">{label}</h3>
          <ul className="space-y-2">
            {questions[key].map((q, i) => {
              const id = `${key}-${i}`;
              return (
                <li key={id} className="border border-zinc-200 dark:border-zinc-700 rounded-lg overflow-hidden">
                  <button
                    className="w-full flex items-start gap-3 px-4 py-3 text-left text-sm hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
                    onClick={() => setOpenIdx(openIdx === id ? null : id)}
                  >
                    <span className="text-zinc-400 font-mono mt-0.5">Q{i + 1}</span>
                    <span className="flex-1 text-zinc-700 dark:text-zinc-300">{q.question}</span>
                    <span className="shrink-0 text-zinc-400 text-xs">{openIdx === id ? "收起" : "回答思路"}</span>
                  </button>
                  {openIdx === id && (
                    <div className="px-4 pb-3 pl-10 text-sm text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-t border-zinc-100 dark:border-zinc-700">
                      {q.hint}
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </div>
  );
}
