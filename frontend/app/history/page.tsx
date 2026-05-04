import { getHistory } from "@/lib/api";
import { AnalysisList } from "@/components/history/analysis-list";

export const dynamic = "force-dynamic";

export default async function HistoryPage() {
  let items = [];
  try {
    items = await getHistory();
  } catch {
    // backend not available during build — render empty
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-10 space-y-6">
      <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">历史分析记录</h1>
      <AnalysisList items={items} />
    </div>
  );
}
