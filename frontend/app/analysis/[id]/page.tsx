"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { toast } from "sonner";
import { getAnalysisStatus, getAnalysisResult } from "@/lib/api";
import type { AnalysisResult } from "@/lib/types";
import { ScoreCard } from "@/components/analysis/score-card";
import { MatchReportPanel } from "@/components/analysis/match-report";
import { InterviewPanel } from "@/components/analysis/interview-panel";
import { IntroPanel } from "@/components/analysis/intro-panel";

const STEPS = ["JD 解析", "匹配分析", "面试题生成", "自我介绍生成"];
const TABS = ["优势与 Gap", "面试题", "自我介绍"] as const;
type Tab = typeof TABS[number];

export default function AnalysisPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [status, setStatus] = useState<string>("pending");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [tab, setTab] = useState<Tab>("优势与 Gap");

  useEffect(() => {
    let timer: ReturnType<typeof setInterval>;
    let elapsed = 0;

    const poll = async () => {
      elapsed += 3;
      if (elapsed > 300) {
        clearInterval(timer);
        toast.error("分析超时，请重试");
        return;
      }
      try {
        const s = await getAnalysisStatus(Number(id));
        setStatus(s.status);
        if (s.status === "done") {
          clearInterval(timer);
          const r = await getAnalysisResult(Number(id));
          setResult(r);
        } else if (s.status === "failed") {
          clearInterval(timer);
          toast.error("分析失败，请重试");
        }
      } catch {
        clearInterval(timer);
      }
    };

    poll();
    timer = setInterval(poll, 3000);
    return () => clearInterval(timer);
  }, [id]);

  if (!result) {
    const stepIndex =
      status === "pending" ? 0 : status === "running" ? 1 : status === "done" ? 4 : 0;
    return (
      <div className="max-w-xl mx-auto px-4 py-20 space-y-10 text-center">
        <h2 className="text-xl font-semibold text-zinc-800 dark:text-zinc-200">AI 分析中，请稍候...</h2>
        <ol className="space-y-3 text-left">
          {STEPS.map((step, i) => (
            <li key={step} className="flex items-center gap-3 text-sm">
              <span
                className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                  i < stepIndex
                    ? "bg-emerald-500 text-white"
                    : i === stepIndex
                    ? "bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 animate-pulse"
                    : "bg-zinc-200 dark:bg-zinc-700 text-zinc-400"
                }`}
              >
                {i < stepIndex ? "✓" : i + 1}
              </span>
              <span
                className={
                  i <= stepIndex
                    ? "text-zinc-800 dark:text-zinc-200"
                    : "text-zinc-400"
                }
              >
                {step}
              </span>
            </li>
          ))}
        </ol>
      </div>
    );
  }

  const { match_report, interview_questions, intro_zh, intro_en } = result;

  return (
    <div className="max-w-5xl mx-auto px-4 py-10 space-y-8">
      {/* Score Header */}
      <div className="flex flex-col items-center gap-4">
        {match_report && <ScoreCard score={match_report.score} />}
        <div className="flex gap-2">
          <button
            onClick={() => router.push("/")}
            className="px-4 py-2 text-sm border border-zinc-300 dark:border-zinc-700 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            重新分析
          </button>
          <button
            onClick={() => window.print()}
            className="px-4 py-2 text-sm bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 rounded-lg hover:bg-zinc-700 dark:hover:bg-zinc-300 transition-colors"
          >
            导出报告
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-zinc-200 dark:border-zinc-700">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors ${
              tab === t
                ? "border-zinc-900 dark:border-zinc-100 text-zinc-900 dark:text-zinc-100"
                : "border-transparent text-zinc-500 hover:text-zinc-700"
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div>
        {tab === "优势与 Gap" && match_report && <MatchReportPanel report={match_report} />}
        {tab === "面试题" && interview_questions && <InterviewPanel questions={interview_questions} />}
        {tab === "自我介绍" && intro_zh && intro_en && <IntroPanel zh={intro_zh} en={intro_en} />}
      </div>
    </div>
  );
}
