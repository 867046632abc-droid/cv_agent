import pytest
import pytest_asyncio
from unittest.mock import MagicMock, AsyncMock
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.database import Base, get_db
from app.main import app
from app.models.schemas import (
    JDProfile, MatchReport, GapItem, InterviewQuestions, InterviewQuestion, Intro, GraphState
)

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def mock_jd_profile() -> JDProfile:
    return JDProfile(
        hard_requirements=["Python", "LangGraph", "FastAPI"],
        nice_to_have=["TypeScript", "Docker"],
        responsibilities=["Build LLM applications", "Design Agent workflows"],
        culture_signals=["Fast-paced", "Remote-friendly"],
        role_tags=["Agent", "Backend"],
        reasoning="Extracted from JD text.",
    )


@pytest.fixture
def mock_match_report() -> MatchReport:
    return MatchReport(
        score=82,
        strengths=["Strong LangGraph experience", "RAG system background"],
        gaps=[GapItem(gap="TypeScript proficiency", mitigation="Mention frontend exposure and quick learning")],
        reasoning="Candidate has strong backend and AI skills.",
    )


@pytest.fixture
def mock_interview_questions() -> InterviewQuestions:
    return InterviewQuestions(
        technical=[InterviewQuestion(question="Explain how LangGraph manages state.", hint="Focus on StateGraph and checkpointers.")],
        project=[InterviewQuestion(question="Walk me through your GraphRAG system.", hint="Mention dual-retrieval and RAGAS evaluation.")],
        gap=[InterviewQuestion(question="How comfortable are you with TypeScript?", hint="Acknowledge current level and highlight transferable skills.")],
    )


@pytest.fixture
def mock_graph_state(mock_jd_profile, mock_match_report, mock_interview_questions) -> GraphState:
    return GraphState(
        jd_text="We are looking for an LLM engineer...",
        resume_text="Experienced in LangGraph, RAG, FastAPI...",
        jd_profile=mock_jd_profile,
        match_report=mock_match_report,
        interview_questions=mock_interview_questions,
        intro=Intro(zh="你好，我是程云杨...", en="Hello, I am Cheng Yunyang..."),
    )
