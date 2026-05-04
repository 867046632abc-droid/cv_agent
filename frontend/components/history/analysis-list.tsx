import Link from "next/link";
import type { HistoryItem } from "@/lib/types";
import { cn } from "@/lib/utils";

const STATUS_LABEL: Record<string, string> = {
  done: "完成",
  running: "分析中",
  pending: "等待中",
  failed: "失败",
};

const STATUS_COLOR: Record<string, string> = {
  done: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-300",
  running: "bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300",
  pending: "bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400",
  failed: "bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-300",
};

export function AnalysisList({ items }: { items: HistoryItem[] }) {
  if (items.length === 0) {
    return (
      <div className="text-center py-20 text-zinc-400">
        <p className="text-lg">暂无分析记录</p>
        <Link href="/" className="mt-2 inline-block text-sm text-zinc-500 hover:text-zinc-800 underline">
          去分析一个 JD
        </Link>
      </div>
    );
  }

  return (
    <ul className="space-y-2">
      {items.map((item) => (
        <li key={item.analysis_id}>
          <Link
            href={`/analysis/${item.analysis_id}`}
            className="flex items-center justify-between gap-4 px-4 py-3 rounded-xl border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
          >
            <div className="min-w-0 flex-1">
              <p className="text-sm text-zinc-700 dark:text-zinc-300 truncate">{item.jd_preview}</p>
              <p className="text-xs text-zinc-400 mt-0.5">
                {new Date(item.created_at).toLocaleString("zh-CN")}
              </p>
            </div>
            <div className="flex items-center gap-3 shrink-0">
              {item.score !== null && (
                <span className="text-sm font-semibold text-zinc-700 dark:text-zinc-200">
                  {item.score}<span className="text-zinc-400 font-normal text-xs">/100</span>
                </span>
              )}
              <span className={cn("text-xs px-2 py-0.5 rounded-full font-medium", STATUS_COLOR[item.status] ?? STATUS_COLOR.pending)}>
                {STATUS_LABEL[item.status] ?? item.status}
              </span>
            </div>
          </Link>
        </li>
      ))}
    </ul>
  );
}
