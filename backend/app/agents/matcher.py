import json
from langchain_openai import ChatOpenAI
from app.models.schemas import GraphState, MatchReport
import os

_llm = ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-4o"), temperature=0)
_structured = _llm.with_structured_output(MatchReport)

_SYSTEM = """You are a technical hiring expert. Compare the candidate's resume against the job requirements.
Score 0-100 honestly. For each gap, provide a concrete mitigation strategy the candidate can use in the interview.
Be specific — avoid generic advice like "learn more about X"."""


def analyze_match(state: GraphState) -> GraphState:
    jd_summary = json.dumps(state.jd_profile.model_dump(), ensure_ascii=False, indent=2)
    result: MatchReport = _structured.invoke([
        {"role": "system", "content": _SYSTEM},
        {
            "role": "user",
            "content": (
                f"Job Requirements (structured):\n{jd_summary}\n\n"
                f"Candidate Resume:\n{state.resume_text}"
            ),
        },
    ])
    return GraphState(**{**state.model_dump(), "match_report": result})
