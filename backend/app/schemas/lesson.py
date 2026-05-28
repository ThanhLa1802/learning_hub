import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.lesson import LessonContentType


class LessonSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    content_type: LessonContentType
    order_index: int
    estimated_minutes: int
    is_completed: bool = False


class LessonResponse(LessonSummaryResponse):
    course_id: uuid.UUID
    category_id: Optional[uuid.UUID]
    content: str
    quiz_id: Optional[uuid.UUID] = None
    is_completed: bool = False
    quiz_passed: bool = True  # True when no quiz exists
    next_lesson_id: Optional[uuid.UUID] = None


class AIExplainRequest(BaseModel):
    question: str = ""


class AIExplainResponse(BaseModel):
    explanation: str
    key_points: list[str]
    real_world_example: str
    interview_tip: str
