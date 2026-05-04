from datetime import datetime
from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    resume_id: Mapped[int] = mapped_column(Integer, ForeignKey("resumes.id"), index=True)
    jd_text: Mapped[str] = mapped_column(Text)
    jd_profile: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    match_report: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    interview_questions: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    intro_zh: Mapped[str | None] = mapped_column(Text, nullable=True)
    intro_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending/running/done/failed
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
