import json
from langchain_openai import ChatOpenAI
from app.models.schemas import GraphState, InterviewQuestions
import os

_llm = ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-4o"), temperature=0.3)
_structured = _llm.with_structured_output(InterviewQuestions)

_SYSTEM = """You are an experienced technical interviewer. Generate targeted interview questions.
- Technical questions: probe deep understanding of the JD's core tech stack
- Project questions: dig into the candidate's specific projects on their resume
- Gap questions: probe the identified weak areas without being obvious
Each question must have a practical answer hint (2-3 sentences max)."""


def gen_interview(state: GraphState) -> GraphState:
    jd_summary = json.dumps(state.jd_profile.model_dump(), ensure_ascii=False, indent=2)
    match_summary = json.dumps(state.match_report.model_dump(), ensure_ascii=False, indent=2)
    result: InterviewQuestions = _structured.invoke([
        {"role": "system", "content": _SYSTEM},
        {
            "role": "user",
            "content": (
                f"JD Profile:\n{jd_summary}\n\n"
                f"Match Analysis:\n{match_summary}\n\n"
                f"Resume:\n{state.resume_text}"
            ),
        },
    ])
    return GraphState(**{**state.model_dump(), "interview_questions": result})
