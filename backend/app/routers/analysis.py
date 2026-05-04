from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.schemas import (
    AnalysisStartRequest, AnalysisStartResponse,
    AnalysisStatusResponse, AnalysisResultResponse,
    AnalysisHistoryItem, JDProfile, MatchReport, InterviewQuestions,
)
from app.services import analysis_service

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.post("/start", response_model=AnalysisStartResponse)
async def start_analysis(
    payload: AnalysisStartRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    resume = await analysis_service.get_resume(db, payload.resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if not payload.jd_text.strip():
        raise HTTPException(status_code=400, detail="JD text cannot be empty")

    analysis = await analysis_service.create_analysis(db, payload.resume_id, payload.jd_text)
    background_tasks.add_task(
        analysis_service.run_analysis_task,
        analysis.id,
        payload.jd_text,
        resume.raw_text,
    )
    return AnalysisStartResponse(analysis_id=analysis.id)


@router.get("/{analysis_id}/status", response_model=AnalysisStatusResponse)
async def get_status(analysis_id: int, db: AsyncSession = Depends(get_db)):
    analysis = await analysis_service.get_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return AnalysisStatusResponse(
        analysis_id=analysis.id,
        status=analysis.status,
        progress_label=analysis_service.progress_label(analysis.status),
    )


@router.get("/{analysis_id}/result", response_model=AnalysisResultResponse)
async def get_result(analysis_id: int, db: AsyncSession = Depends(get_db)):
    analysis = await analysis_service.get_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    if analysis.status == "failed":
        raise HTTPException(status_code=422, detail=analysis.error_message or "Analysis failed")
    if analysis.status != "done":
        raise HTTPException(status_code=202, detail="Analysis not complete yet")

    return AnalysisResultResponse(
        analysis_id=analysis.id,
        status=analysis.status,
        jd_profile=JDProfile(**analysis.jd_profile) if analysis.jd_profile else None,
        match_report=MatchReport(**analysis.match_report) if analysis.match_report else None,
        interview_questions=InterviewQuestions(**analysis.interview_questions) if analysis.interview_questions else None,
        intro_zh=analysis.intro_zh,
        intro_en=analysis.intro_en,
    )


@router.get("/history", response_model=list[AnalysisHistoryItem])
async def get_history(db: AsyncSession = Depends(get_db)):
    records = await analysis_service.get_history(db)
    return [
        AnalysisHistoryItem(
            analysis_id=r.id,
            jd_preview=r.jd_text[:60] + "..." if len(r.jd_text) > 60 else r.jd_text,
            score=r.match_report.get("score") if r.match_report else None,
            status=r.status,
            created_at=r.created_at.isoformat(),
        )
        for r in records
    ]
