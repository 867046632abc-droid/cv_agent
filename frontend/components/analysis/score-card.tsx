import { cn } from "@/lib/utils";

interface Props {
  score: number;
}

export function ScoreCard({ score }: Props) {
  const color =
    score >= 80 ? "text-emerald-600" : score >= 60 ? "text-amber-500" : "text-red-500";
  const ringColor =
    score >= 80 ? "stroke-emerald-500" : score >= 60 ? "stroke-amber-400" : "stroke-red-400";

  const r = 54;
  const circumference = 2 * Math.PI * r;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="140" height="140" className="-rotate-90">
        <circle cx="70" cy="70" r={r} fill="none" stroke="#e4e4e7" strokeWidth="10" />
        <circle
          cx="70" cy="70" r={r} fill="none" strokeWidth="10"
          strokeDasharray={circumference} strokeDashoffset={offset}
          strokeLinecap="round"
          className={cn("transition-all duration-700", ringColor)}
        />
      </svg>
      <div className="text-center -mt-20">
        <span className={cn("text-5xl font-bold", color)}>{score}</span>
        <span className="text-zinc-400 text-lg">/100</span>
      </div>
      <p className="mt-16 text-sm text-zinc-500">综合匹配分数</p>
    </div>
  );
}
