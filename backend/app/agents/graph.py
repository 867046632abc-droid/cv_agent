from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.models.schemas import GraphState
from app.agents.jd_parser import parse_jd
from app.agents.matcher import analyze_match
from app.agents.interview_gen import gen_interview
from app.agents.intro_gen import gen_intro


def _safe_node(fn):
    def wrapper(state: GraphState) -> GraphState:
        try:
            return fn(state)
        except Exception as e:
            return GraphState(**{**state.model_dump(), "error": str(e)})
    wrapper.__name__ = fn.__name__
    return wrapper


def _should_continue(state: GraphState) -> str:
    return END if state.error else "continue"


def build_graph() -> StateGraph:
    builder = StateGraph(GraphState)

    builder.add_node("parse_jd", _safe_node(parse_jd))
    builder.add_node("analyze_match", _safe_node(analyze_match))
    builder.add_node("gen_interview", _safe_node(gen_interview))
    builder.add_node("gen_intro", _safe_node(gen_intro))

    builder.set_entry_point("parse_jd")
    builder.add_conditional_edges("parse_jd", _should_continue, {END: END, "continue": "analyze_match"})
    builder.add_conditional_edges("analyze_match", _should_continue, {END: END, "continue": "gen_interview"})
    builder.add_conditional_edges("gen_interview", _should_continue, {END: END, "continue": "gen_intro"})
    builder.add_edge("gen_intro", END)

    return builder.compile(checkpointer=MemorySaver())


_graph = build_graph()


def run_pipeline(jd_text: str, resume_text: str) -> GraphState:
    initial = GraphState(jd_text=jd_text, resume_text=resume_text)
    config = {"configurable": {"thread_id": "pipeline"}}
    result = _graph.invoke(initial, config=config)
    return GraphState(**result)
