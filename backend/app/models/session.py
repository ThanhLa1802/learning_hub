import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from app.models.scenario import PracticeMode


class SessionStatus(str, Enum):
    in_progress = "in_progress"
    completed = "completed"


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class PracticeSession(SQLModel, table=True):
    __tablename__ = "practice_sessions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    scenario_id: uuid.UUID = Field(foreign_key="scenarios.id", index=True)
    mode: PracticeMode
    status: SessionStatus = Field(default=SessionStatus.in_progress)
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = Field(default=None)
    overall_score: Optional[int] = Field(default=None)
    ai_feedback: Optional[dict] = Field(default=None, sa_column=Column(JSONB, nullable=True))


class SessionMessage(SQLModel, table=True):
    __tablename__ = "session_messages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_id: uuid.UUID = Field(foreign_key="practice_sessions.id", index=True)
    role: MessageRole
    content: str = Field(sa_column=Column(Text))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
