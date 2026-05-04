import type { AnalysisResult, AnalysisStatus, HistoryItem } from "./types";

const BASE = "/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...init?.headers },
    ...init,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? "Request failed");
  }
  return res.json() as Promise<T>;
}

export async function uploadResume(file: File): Promise<{ resume_id: number; filename: string }> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE}/resume/upload`, { method: "POST", body: form });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? "Upload failed");
  }
  return res.json();
}

export async function startAnalysis(
  resume_id: number,
  jd_text: string
): Promise<{ analysis_id: number }> {
  return request("/analysis/start", {
    method: "POST",
    body: JSON.stringify({ resume_id, jd_text }),
  });
}

export async function getAnalysisStatus(analysis_id: number): Promise<AnalysisStatus> {
  return request(`/analysis/${analysis_id}/status`);
}

export async function getAnalysisResult(analysis_id: number): Promise<AnalysisResult> {
  return request(`/analysis/${analysis_id}/result`);
}

export async function getHistory(): Promise<HistoryItem[]> {
  return request("/analysis/history");
}
