import uuid

from pydantic import BaseModel, ConfigDict

from app.models.scenario import Difficulty, PracticeMode


class ScenarioCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    title: str
    description: str
    icon_name: str
    order_index: int
    course_id: uuid.UUID | None = None


class ScenarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    category_id: uuid.UUID
    title: str
    description: str
    mode: PracticeMode
    difficulty: Difficulty
    tags: list[str]
    order_index: int
    is_active: bool
    category: ScenarioCategoryResponse | None = None
