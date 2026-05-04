"use client";
import { useState } from "react";
import type { MatchReport } from "@/lib/types";

export function MatchReportPanel({ report }: { report: MatchReport }) {
  const [openIdx, setOpenIdx] = useState<number | null>(null);

  return (
    <div className="space-y-6">
      {/* Strengths */}
      <div>
        <h3 className="font-semibold text-zinc-800 dark:text-zinc-200 mb-3">优势项</h3>
        <ul className="space-y-2">
          {report.strengths.map((s, i) => (
            <li key={i} className="flex items-start gap-2 text-sm">
              <span className="mt-0.5 text-emerald-500">✓</span>
              <span className="text-zinc-700 dark:text-zinc-300">{s}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Gaps */}
      <div>
        <h3 className="font-semibold text-zinc-800 dark:text-zinc-200 mb-3">Gap 分析</h3>
        <ul className="space-y-2">
          {report.gaps.map((g, i) => (
            <li key={i} className="border border-zinc-200 dark:border-zinc-700 rounded-lg overflow-hidden">
              <button
                className="w-full flex items-center justify-between px-4 py-3 text-left text-sm hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
                onClick={() => setOpenIdx(openIdx === i ? null : i)}
              >
                <span className="flex items-center gap-2">
                  <span className="text-amber-500">⚠</span>
                  <span className="text-zinc-700 dark:text-zinc-300">{g.gap}</span>
                </span>
                <span className="text-zinc-400 text-xs">{openIdx === i ? "收起" : "应对建议"}</span>
              </button>
              {openIdx === i && (
                <div className="px-4 pb-3 text-sm text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-t border-zinc-100 dark:border-zinc-700">
                  {g.mitigation}
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
