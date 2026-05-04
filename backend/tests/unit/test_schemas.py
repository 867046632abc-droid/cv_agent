import pytest
from pydantic import ValidationError
from app.models.schemas import JDProfile, MatchReport, GapItem, InterviewQuestions, InterviewQuestion, Intro


def test_jd_profile_valid(mock_jd_profile):
    assert isinstance(mock_jd_profile.hard_requirements, list)
    assert len(mock_jd_profile.role_tags) > 0
    assert isinstance(mock_jd_profile.reasoning, str)


def test_match_report_score_bounds():
    with pytest.raises(ValidationError):
        MatchReport(score=101, strengths=[], gaps=[], reasoning="x")
    with pytest.raises(ValidationError):
        MatchReport(score=-1, strengths=[], gaps=[], reasoning="x")


def test_match_report_valid(mock_match_report):
    assert 0 <= mock_match_report.score <= 100
    assert isinstance(mock_match_report.strengths, list)
    assert all(isinstance(g, GapItem) for g in mock_match_report.gaps)


def test_gap_item_requires_mitigation():
    with pytest.raises(ValidationError):
        GapItem(gap="TypeScript")  # missing mitigation


def test_interview_questions_structure(mock_interview_questions):
    assert isinstance(mock_interview_questions.technical, list)
    assert isinstance(mock_interview_questions.project, list)
    assert isinstance(mock_interview_questions.gap, list)
    for q in mock_interview_questions.technical + mock_interview_questions.project + mock_interview_questions.gap:
        assert isinstance(q, InterviewQuestion)
        assert q.question and q.hint


def test_intro_both_languages():
    intro = Intro(zh="中文自我介绍", en="English self-introduction")
    assert intro.zh and intro.en
