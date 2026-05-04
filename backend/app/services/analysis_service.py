import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.analysis import Analysis
from app.models.resume import Resume
from app.agents.graph import run_pipeline

_STATUS_LABELS = {
    "pending": "等待开始",
    "running": "AI 分析中",
    "done": "分析完成",
    "failed": "分析失败",
}


async def get_resume(db: AsyncSession, resume_id: int) -> Resume | None:
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    return result.scalar_one_or_none()


async def create_analysis(db: AsyncSession, resume_id: int, jd_text: str) -> Analysis:
    analysis = Analysis(resume_id=resume_id, jd_text=jd_text, status="pending")
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    return analysis


async def get_analysis(db: AsyncSession, analysis_id: int) -> Analysis | None:
    result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
    return result.scalar_one_or_none()


async def get_history(db: AsyncSession, limit: int = 20) -> list[Analysis]:
    result = await db.execute(select(Analysis).order_by(desc(Analysis.created_at)).limit(limit))
    return list(result.scalars().all())


def progress_label(status: str) -> str:
    return _STATUS_LABELS.get(status, status)


async def run_analysis_task(analysis_id: int, jd_text: str, resume_text: str) -> None:
    from app.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        analysis = await get_analysis(db, analysis_id)
        if not analysis:
            return

        analysis.status = "running"
        await db.commit()

        try:
            # LangGraph blocks — run in thread to avoid blocking the event loop
            state = await asyncio.get_event_loop().run_in_executor(
                None, run_pipeline, jd_text, resume_text
            )

            if state.error:
                analysis.status = "failed"
                analysis.error_message = state.error
            else:
                analysis.status = "done"
                analysis.jd_profile = state.jd_profile.model_dump() if state.jd_profile else None
                analysis.match_report = state.match_report.model_dump() if state.match_report else None
                analysis.interview_questions = (
                    state.interview_questions.model_dump() if state.interview_questions else None
                )
                analysis.intro_zh = state.intro.zh if state.intro else None
                analysis.intro_en = state.intro.en if state.intro else None

        except Exception as e:
            analysis.status = "failed"
            analysis.error_message = str(e)

        await db.commit()
