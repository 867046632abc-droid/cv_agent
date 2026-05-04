import json
from app.models.schemas import GraphState, Intro
from app.agents.utils import get_llm, parse_json_response

_llm = get_llm(temperature=0.5)

_SYSTEM = """你是一位求职辅导专家。根据简历和JD，生成自我介绍，并ONLY以JSON格式回复。
不要有任何markdown、解释或其他文字，只输出JSON对象，包含以下键：
- zh: 字符串，中文自我介绍，结构为：个人背景(100字) + 核心项目亮点(250字) + 求职动机(100字)
- en: 字符串，英文自我介绍，150-200词，相同三段结构"""


def gen_intro(state: GraphState) -> GraphState:
    jd_summary = json.dumps(state.jd_profile.model_dump(), ensure_ascii=False, indent=2)
    strengths = json.dumps(state.match_report.strengths, ensure_ascii=False)
    resp = _llm.invoke([
        {"role": "system", "content": _SYSTEM},
        {"role": "user", "content": f"JD核心要求：\n{jd_summary}\n\n匹配优势：\n{strengths}\n\n简历：\n{state.resume_text}"},
    ])
    result = parse_json_response(resp.content, Intro)
    return GraphState(**{**state.model_dump(), "intro": result})
