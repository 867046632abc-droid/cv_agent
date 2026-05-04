"use client";
import { useEffect, useState, useRef } from "react";
import { getAnalysisStatus, getAnalysisResult } from "@/lib/api";
import type { AnalysisResult, AnalysisStatus } from "@/lib/types";

const TIMEOUT_SECONDS = 300;
const POLL_INTERVAL = 3000;

export function useAnalysisPoller(analysisId: number | null) {
  const [status, setStatus] = useState<AnalysisStatus["status"]>("pending");
  const [progressLabel, setProgressLabel] = useState("等待开始");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [timedOut, setTimedOut] = useState(false);
  const elapsed = useRef(0);

  useEffect(() => {
    if (!analysisId) return;
    elapsed.current = 0;
    setStatus("pending");
    setResult(null);
    setTimedOut(false);

    const poll = async () => {
      elapsed.current += POLL_INTERVAL / 1000;
      if (elapsed.current > TIMEOUT_SECONDS) {
        setTimedOut(true);
        clearInterval(timer);
        return;
      }
      try {
        const s = await getAnalysisStatus(analysisId);
        setStatus(s.status);
        setProgressLabel(s.progress_label);
        if (s.status === "done") {
          clearInterval(timer);
          const r = await getAnalysisResult(analysisId);
          setResult(r);
        } else if (s.status === "failed") {
          clearInterval(timer);
        }
      } catch {
        clearInterval(timer);
      }
    };

    poll();
    const timer = setInterval(poll, POLL_INTERVAL);
    return () => clearInterval(timer);
  }, [analysisId]);

  return { status, progressLabel, result, timedOut };
}
