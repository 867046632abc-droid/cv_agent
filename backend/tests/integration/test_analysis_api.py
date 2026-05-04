import io
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.models.resume import Resume
from app.models.analysis import Analysis


async def _seed_resume(db_session) -> int:
    resume = Resume(user_session="test-session", filename="test.pdf", raw_text="Python LangGraph developer")
    db_session.add(resume)
    await db_session.commit()
    await db_session.refresh(resume)
    return resume.id


@pytest.mark.asyncio
async def test_start_analysis_returns_id(client, db_session):
    resume_id = await _seed_resume(db_session)
    with patch("app.routers.analysis.analysis_service.run_analysis_task", new_callable=AsyncMock):
        response = await client.post(
            "/api/analysis/start",
            json={"resume_id": resume_id, "jd_text": "We need a Python engineer with LangGraph experience."},
        )
    assert response.status_code == 200
    assert "analysis_id" in response.json()


@pytest.mark.asyncio
async def test_start_analysis_invalid_resume(client):
    response = await client.post(
        "/api/analysis/start",
        json={"resume_id": 9999, "jd_text": "Some JD text"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_status_pending(client, db_session):
    resume_id = await _seed_resume(db_session)
    with patch("app.routers.analysis.analysis_service.run_analysis_task", new_callable=AsyncMock):
        start = await client.post(
            "/api/analysis/start",
            json={"resume_id": resume_id, "jd_text": "JD text"},
        )
    analysis_id = start.json()["analysis_id"]
    response = await client.get(f"/api/analysis/{analysis_id}/status")
    assert response.status_code == 200
    assert response.json()["status"] in ("pending", "running", "done", "failed")


@pytest.mark.asyncio
async def test_history_returns_list(client, db_session):
    response = await client.get("/api/analysis/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
