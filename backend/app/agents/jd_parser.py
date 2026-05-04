from langchain_openai import ChatOpenAI
from app.models.schemas import GraphState, JDProfile
import os

_llm = ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-4o"), temperature=0)
_structured = _llm.with_structured_output(JDProfile)

_SYSTEM = """You are a senior technical recruiter. Analyze the given job description and extract structured information.
Be precise. Culture signals should reflect implicit expectations (e.g., "fast-paced", "independent worker", "strong communicator").
Role tags should be concise labels like: RAG, Agent, Backend, Algorithm, Full-Stack, DevOps, etc."""


def parse_jd(state: GraphState) -> GraphState:
    result: JDProfile = _structured.invoke([
        {"role": "system", "content": _SYSTEM},
        {"role": "user", "content": f"Job Description:\n\n{state.jd_text}"},
    ])
    return GraphState(**{**state.model_dump(), "jd_profile": result})
