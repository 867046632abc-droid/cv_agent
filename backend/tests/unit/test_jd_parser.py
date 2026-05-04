from unittest.mock import patch
from app.models.schemas import GraphState, JDProfile
from app.agents.jd_parser import parse_jd


def _mock_jd_profile():
    return JDProfile(
        hard_requirements=["Python", "LangGraph"],
        nice_to_have=["Docker"],
        responsibilities=["Build AI systems"],
        culture_signals=["Fast-paced"],
        role_tags=["Agent"],
        reasoning="Test reasoning",
    )


def test_parse_jd_returns_state_with_profile():
    state = GraphState(jd_text="We need a Python LangGraph engineer.", resume_text="")
    with patch("app.agents.jd_parser._structured") as mock_llm:
        mock_llm.invoke.return_value = _mock_jd_profile()
        result = parse_jd(state)

    assert result.jd_profile is not None
    assert isinstance(result.jd_profile.hard_requirements, list)
    assert "Python" in result.jd_profile.hard_requirements
    assert result.error is None


def test_parse_jd_preserves_other_state_fields():
    state = GraphState(jd_text="JD text", resume_text="My resume")
    with patch("app.agents.jd_parser._structured") as mock_llm:
        mock_llm.invoke.return_value = _mock_jd_profile()
        result = parse_jd(state)

    assert result.resume_text == "My resume"
    assert result.jd_text == "JD text"


def test_parse_jd_all_fields_present():
    state = GraphState(jd_text="JD", resume_text="")
    with patch("app.agents.jd_parser._structured") as mock_llm:
        mock_llm.invoke.return_value = _mock_jd_profile()
        result = parse_jd(state)

    profile = result.jd_profile
    assert profile.hard_requirements is not None
    assert profile.nice_to_have is not None
    assert profile.responsibilities is not None
    assert profile.culture_signals is not None
    assert profile.role_tags is not None
    assert profile.reasoning != ""
