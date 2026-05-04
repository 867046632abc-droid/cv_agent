import json
from langchain_openai import ChatOpenAI
from app.models.schemas import GraphState, Intro
import os

_llm = ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-4o"), temperature=0.5)
_structured = _llm.with_structured_output(Intro)

_SYSTEM_ZH = """你是一位求职辅导专家，请根据简历和JD撰写一段2分钟的中文自我介绍草稿。
结构：
1. 个人背景（约100字）：学历、专业方向、核心技术栈
2. 核心项目亮点（约250字）：优先展示与JD最匹配的1-2个项目，突出量化成果
3. 求职动机（约100字）：为何对该岗位感兴趣，能带来什么价值
语气专业自然，避免空洞套话。

英文版结构相同，约150-200词，语气正式但不生硬。"""


def gen_intro(state: GraphState) -> GraphState:
    jd_summary = json.dumps(state.jd_profile.model_dump(), ensure_ascii=False, indent=2)
    strengths = json.dumps(state.match_report.strengths, ensure_ascii=False)
    result: Intro = _structured.invoke([
        {"role": "system", "content": _SYSTEM_ZH},
        {
            "role": "user",
            "content": (
                f"JD核心要求：\n{jd_summary}\n\n"
                f"简历匹配优势：\n{strengths}\n\n"
                f"候选人简历：\n{state.resume_text}"
            ),
        },
    ])
    return GraphState(**{**state.model_dump(), "intro": result})
