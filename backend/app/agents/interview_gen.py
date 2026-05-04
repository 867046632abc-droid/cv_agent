import json
from app.models.schemas import GraphState, InterviewQuestions
from app.agents.utils import get_llm, parse_json_response

_llm = get_llm(temperature=0.3)

_SYSTEM = """You are an experienced technical interviewer. Generate interview questions and respond ONLY with a JSON object.
No markdown, no explanation, just the JSON object with these exact keys:
- technical: array of objects, each with "question" (string) and "hint" (string)
- project: array of objects, each with "question" (string) and "hint" (string)
- gap: array of objects, each with "question" (string) and "hint" (string)
Generate 3-4 items per category."""


def gen_interview(state: GraphState) -> GraphState:
    jd_summary = json.dumps(state.jd_profile.model_dump(), ensure_ascii=False, indent=2)
    match_summary = json.dumps(state.match_report.model_dump(), ensure_ascii=False, indent=2)
    resp = _llm.invoke([
        {"role": "system", "content": _SYSTEM},
        {"role": "user", "content": f"JD:\n{jd_summary}\n\nMatch Analysis:\n{match_summary}\n\nResume:\n{state.resume_text}"},
    ])
    result = parse_json_response(resp.content, InterviewQuestions)
    return GraphState(**{**state.model_dump(), "interview_questions": result})
