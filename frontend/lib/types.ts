export interface JDProfile {
  hard_requirements: string[];
  nice_to_have: string[];
  responsibilities: string[];
  culture_signals: string[];
  role_tags: string[];
  reasoning: string;
}

export interface GapItem {
  gap: string;
  mitigation: string;
}

export interface MatchReport {
  score: number;
  strengths: string[];
  gaps: GapItem[];
  reasoning: string;
}

export interface InterviewQuestion {
  question: string;
  hint: string;
}

export interface InterviewQuestions {
  technical: InterviewQuestion[];
  project: InterviewQuestion[];
  gap: InterviewQuestion[];
}

export interface AnalysisResult {
  analysis_id: number;
  status: string;
  jd_profile: JDProfile | null;
  match_report: MatchReport | null;
  interview_questions: InterviewQuestions | null;
  intro_zh: string | null;
  intro_en: string | null;
}

export interface AnalysisStatus {
  analysis_id: number;
  status: "pending" | "running" | "done" | "failed";
  progress_label: string;
}

export interface HistoryItem {
  analysis_id: number;
  jd_preview: string;
  score: number | null;
  status: string;
  created_at: string;
}
