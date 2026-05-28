import uuid
from enum import Enum
from typing import Optional

from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class LessonContentType(str, Enum):
    theory = "theory"
    explanation = "explanation"
    case_study = "case_study"


class Lesson(SQLModel, table=True):
    __tablename__ = "lessons"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    course_id: uuid.UUID = Field(foreign_key="courses.id", index=True)
    category_id: Optional[uuid.UUID] = Field(default=None, foreign_key="scenario_categories.id", index=True)
    title: str = Field(max_length=200)
    content: str = Field(sa_column=Column(Text))
    content_type: LessonContentType = Field(default=LessonContentType.theory)
    order_index: int = Field(default=0)
    estimated_minutes: int = Field(default=5)
    is_active: bool = Field(default=True)
    translations: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
