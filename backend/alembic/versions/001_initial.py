"""initial

Revision ID: 001
Revises:
Create Date: 2026-05-04
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "resumes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_session", sa.String(64), nullable=False, index=True),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("raw_text", sa.Text(), nullable=False),
        sa.Column("parsed_content", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "analyses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("resume_id", sa.Integer(), sa.ForeignKey("resumes.id"), nullable=False, index=True),
        sa.Column("jd_text", sa.Text(), nullable=False),
        sa.Column("jd_profile", JSONB(), nullable=True),
        sa.Column("match_report", JSONB(), nullable=True),
        sa.Column("interview_questions", JSONB(), nullable=True),
        sa.Column("intro_zh", sa.Text(), nullable=True),
        sa.Column("intro_en", sa.Text(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("analyses")
    op.drop_table("resumes")
