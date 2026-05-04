from pydantic import BaseModel, Field
from typing import Annotated


# ── JD Parser ──────────────────────────────────────────────────────────────

class JDProfile(BaseModel):
    hard_requirements: list[str] = Field(description="Must-have skills and requirements")
    nice_to_have: list[str] = Field(description="Bonus skills and nice-to-have requirements")
    responsibilities: list[str] = Field(description="Key job responsibilities summary")
    culture_signals: list[str] = Field(description="Implicit culture or work-style signals")
    role_tags: list[str] = Field(description="Role type tags, e.g. RAG, Agent, Backend, Algorithm")
    reasoning: str = Field(description="Step-by-step reasoning for the extraction")


# ── Match Report ────────────────────────────────────────────────────────────

class GapItem(BaseModel):
    gap: str = Field(description="Skill or requirement that is missing or weak in the resume")
    mitigation: str = Field(description="How to address this gap in an interview")


class MatchReport(BaseModel):
    score: Annotated[int, Field(ge=0, le=100)] = Field(description="Overall match score 0-100")
    strengths: list[str] = Field(description="Resume points that strongly match the JD")
    gaps: list[GapItem] = Field(description="JD requirements missing or weak in resume")
    reasoning: str = Field(description="Step-by-step reasoning for the score")


# ── Interview Questions ─────────────────────────────────────────────────────

class InterviewQuestion(BaseModel):
    question: str
    hint: str = Field(description="Answer approach hint for the candidate")


class InterviewQuestions(BaseModel):
    technical: list[InterviewQuestion] = Field(description="Deep-dive technical questions based on JD core stack")
    project: list[InterviewQuestion] = Field(description="Project experience questions based on resume")
    gap: list[InterviewQuestion] = Field(description="Questions targeting identified resume gaps")


# ── Self Introduction ───────────────────────────────────────────────────────

class Intro(BaseModel):
    zh: str = Field(description="Chinese self-introduction, 400-500 characters, 3-paragraph structure")
    en: str = Field(description="English self-introduction, 150-200 words, 3-paragraph structure")


# ── Graph State ─────────────────────────────────────────────────────────────

class GraphState(BaseModel):
    jd_text: str
    resume_text: str
    jd_profile: JDProfile | None = None
    match_report: MatchReport | None = None
    interview_questions: InterviewQuestions | None = None
    intro: Intro | None = None
    error: str | None = None


# ── API Request / Response schemas ─────────────────────────────────────────

class ResumeUploadResponse(BaseModel):
    resume_id: int
    filename: str


class AnalysisStartRequest(BaseModel):
    resume_id: int
    jd_text: str


class AnalysisStartResponse(BaseModel):
    analysis_id: int


class AnalysisStatusResponse(BaseModel):
    analysis_id: int
    status: str
    progress_label: str


class AnalysisResultResponse(BaseModel):
    analysis_id: int
    status: str
    jd_profile: JDProfile | None
    match_report: MatchReport | None
    interview_questions: InterviewQuestions | None
    intro_zh: str | None
    intro_en: str | None


class AnalysisHistoryItem(BaseModel):
    analysis_id: int
    jd_preview: str
    score: int | None
    status: str
    created_at: str
