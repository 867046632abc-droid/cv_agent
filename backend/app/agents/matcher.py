import json
from app.models.schemas import GraphState, MatchReport
from app.agents.utils import get_llm, parse_json_response

_llm = get_llm(temperature=0)

_SYSTEM = """You are a technical hiring expert. Compare the resume against the JD and respond ONLY with a JSON object.
No markdown, no explanation, just the JSON object with these exact keys:
- score: integer 0-100
- strengths: array of strings
- gaps: array of objects, each with keys "gap" (string) and "mitigation" (string)
- reasoning: string"""


def analyze_match(state: GraphState) -> GraphState:
    jd_summary = json.dumps(state.jd_profile.model_dump(), ensure_ascii=False, indent=2)
    resp = _llm.invoke([
        {"role": "system", "content": _SYSTEM},
        {"role": "user", "content": f"Job Requirements:\n{jd_summary}\n\nResume:\n{state.resume_text}"},
    ])
    result = parse_json_response(resp.content, MatchReport)
    return GraphState(**{**state.model_dump(), "match_report": result})
