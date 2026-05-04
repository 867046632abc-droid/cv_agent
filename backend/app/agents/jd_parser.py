from app.models.schemas import GraphState, JDProfile
from app.agents.utils import get_llm, parse_json_response

_llm = get_llm(temperature=0)

_SYSTEM = """You are a senior technical recruiter. Analyze the job description and respond ONLY with a JSON object.
No markdown, no explanation, just the JSON object with these exact keys:
- hard_requirements: array of strings
- nice_to_have: array of strings
- responsibilities: array of strings
- culture_signals: array of strings
- role_tags: array of strings (e.g. ["RAG", "Agent", "Backend"])
- reasoning: string"""


def parse_jd(state: GraphState) -> GraphState:
    resp = _llm.invoke([
        {"role": "system", "content": _SYSTEM},
        {"role": "user", "content": f"Job Description:\n\n{state.jd_text}"},
    ])
    result = parse_json_response(resp.content, JDProfile)
    return GraphState(**{**state.model_dump(), "jd_profile": result})
