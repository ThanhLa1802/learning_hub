import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class UserQuizAttempt(SQLModel, table=True):
    __tablename__ = "user_quiz_attempts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    quiz_id: uuid.UUID = Field(foreign_key="quizzes.id", index=True)
    answers: list = Field(sa_column=Column(JSONB))
    score: float = Field(default=0.0)
    completed_at: datetime = Field(default_factory=datetime.utcnow)


class UserLessonProgress(SQLModel, table=True):
    __tablename__ = "user_lesson_progress"
    __table_args__ = (UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson"),)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    lesson_id: uuid.UUID = Field(foreign_key="lessons.id", index=True)
    completed_at: datetime = Field(default_factory=datetime.utcnow)


class UserDomainProgress(SQLModel, table=True):
    __tablename__ = "user_domain_progress"
    __table_args__ = (UniqueConstraint("user_id", "domain_id", name="uq_user_domain"),)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    domain_id: uuid.UUID = Field(foreign_key="domains.id", index=True)
    sessions_completed: int = Field(default=0)
    lessons_completed: int = Field(default=0)
    quizzes_taken: int = Field(default=0)
    avg_quiz_score: float = Field(default=0.0)
    last_activity_at: Optional[datetime] = Field(default=None)
