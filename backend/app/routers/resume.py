import io
import uuid
import pdfplumber
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.resume import Resume
from app.models.schemas import ResumeUploadResponse
from app.core.config import MAX_UPLOAD_SIZE

router = APIRouter(prefix="/api/resume", tags=["resume"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 10 MB limit")

    try:
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            raw_text = "\n".join(page.extract_text() or "" for page in pdf.pages).strip()
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to parse PDF file")

    if not raw_text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    session_id = str(uuid.uuid4())
    resume = Resume(user_session=session_id, filename=file.filename, raw_text=raw_text)
    db.add(resume)
    await db.commit()
    await db.refresh(resume)

    return ResumeUploadResponse(resume_id=resume.id, filename=resume.filename)
