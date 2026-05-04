import io
import pytest
from unittest.mock import patch, MagicMock


def _make_pdf_bytes() -> bytes:
    # Minimal valid-enough bytes for mocking pdfplumber
    return b"%PDF-1.4 fake pdf content"


@pytest.mark.asyncio
async def test_upload_valid_pdf(client):
    mock_pdf = MagicMock()
    mock_pdf.__enter__ = MagicMock(return_value=mock_pdf)
    mock_pdf.__exit__ = MagicMock(return_value=False)
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Experienced Python developer with LangGraph skills."
    mock_pdf.pages = [mock_page]

    with patch("app.routers.resume.pdfplumber.open", return_value=mock_pdf):
        response = await client.post(
            "/api/resume/upload",
            files={"file": ("resume.pdf", io.BytesIO(_make_pdf_bytes()), "application/pdf")},
        )

    assert response.status_code == 200
    data = response.json()
    assert "resume_id" in data
    assert data["filename"] == "resume.pdf"


@pytest.mark.asyncio
async def test_upload_non_pdf_rejected(client):
    response = await client.post(
        "/api/resume/upload",
        files={"file": ("resume.docx", io.BytesIO(b"fake docx"), "application/vnd.openxmlformats")},
    )
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


@pytest.mark.asyncio
async def test_upload_oversized_file(client):
    large_content = b"a" * (11 * 1024 * 1024)  # 11 MB
    mock_pdf = MagicMock()
    with patch("app.routers.resume.pdfplumber.open", return_value=mock_pdf):
        response = await client.post(
            "/api/resume/upload",
            files={"file": ("big.pdf", io.BytesIO(large_content), "application/pdf")},
        )
    assert response.status_code == 400
    assert "10 MB" in response.json()["detail"]
