import uuid
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class Quiz(SQLModel, table=True):
    __tablename__ = "quizzes"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    course_id: uuid.UUID = Field(foreign_key="courses.id", index=True)
    lesson_id: Optional[uuid.UUID] = Field(default=None, foreign_key="lessons.id", index=True)
    title: str = Field(max_length=200)
    description: str = Field(max_length=500, default="")
    order_index: int = Field(default=0)
    translations: Optional[dict] = Field(default=None, sa_column=Column(JSONB))


class QuizQuestion(SQLModel, table=True):
    __tablename__ = "quiz_questions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    quiz_id: uuid.UUID = Field(foreign_key="quizzes.id", index=True)
    question: str = Field(max_length=1000)
    options: list = Field(sa_column=Column(JSONB))
    correct_answer_index: int
    explanation: str = Field(max_length=1000)
    order_index: int = Field(default=0)
    translations: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
