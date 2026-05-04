from unittest.mock import patch
from app.models.schemas import GraphState, MatchReport, GapItem
from app.agents.matcher import analyze_match


def _mock_report(score: int = 75) -> MatchReport:
    return MatchReport(
        score=score,
        strengths=["Strong LangGraph experience"],
        gaps=[GapItem(gap="TypeScript", mitigation="Mention transferable JS knowledge")],
        reasoning="Good overall match",
    )


def _base_state(mock_jd_profile):
    return GraphState(
        jd_text="JD text",
        resume_text="Resume text",
        jd_profile=mock_jd_profile,
    )


def test_analyze_match_score_in_range(mock_jd_profile):
    state = _base_state(mock_jd_profile)
    with patch("app.agents.matcher._structured") as mock_llm:
        mock_llm.invoke.return_value = _mock_report(75)
        result = analyze_match(state)

    assert 0 <= result.match_report.score <= 100


def test_analyze_match_required_fields_present(mock_jd_profile):
    state = _base_state(mock_jd_profile)
    with patch("app.agents.matcher._structured") as mock_llm:
        mock_llm.invoke.return_value = _mock_report()
        result = analyze_match(state)

    report = result.match_report
    assert isinstance(report.strengths, list)
    assert isinstance(report.gaps, list)
    assert report.reasoning != ""


def test_analyze_match_gaps_have_mitigation(mock_jd_profile):
    state = _base_state(mock_jd_profile)
    with patch("app.agents.matcher._structured") as mock_llm:
        mock_llm.invoke.return_value = _mock_report()
        result = analyze_match(state)

    for gap in result.match_report.gaps:
        assert gap.gap
        assert gap.mitigation
