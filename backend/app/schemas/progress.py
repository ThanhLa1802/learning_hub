from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel


class UserDomainProgressResponse(BaseModel):
    domain_id: uuid.UUID
    domain_name: str
    sessions_completed: int
    lessons_completed: int
    total_lessons: int
    quizzes_taken: int
    avg_quiz_score: float
    last_activity_at: Optional[datetime]


class UserProgressResponse(BaseModel):
    domains: list[UserDomainProgressResponse]
