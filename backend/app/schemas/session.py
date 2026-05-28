import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.scenario import PracticeMode
from app.models.session import MessageRole, SessionStatus
from app.schemas.scenario import ScenarioResponse


class CreateSessionRequest(BaseModel):
    scenario_id: uuid.UUID


class AddMessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=5000)


class CompleteSessionRequest(BaseModel):
    user_response: Optional[str] = Field(default=None, max_length=5000)
    lang: str = Field(default="en", max_length=5)


class SessionMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    session_id: uuid.UUID
    role: MessageRole
    content: str
    created_at: datetime


class PracticeSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    scenario_id: uuid.UUID
    mode: PracticeMode
    status: SessionStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    overall_score: Optional[int] = None
    ai_feedback: Optional[dict] = None
    scenario: Optional[ScenarioResponse] = None
    messages: list[SessionMessageResponse] = []


class PaginatedSessionsResponse(BaseModel):
    items: list[PracticeSessionResponse]
    total: int
    skip: int
    limit: int
