import uuid
from enum import Enum
from typing import Optional

from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class PracticeMode(str, Enum):
    text_response = "text_response"
    ai_chat = "ai_chat"


class Difficulty(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class ScenarioCategory(SQLModel, table=True):
    __tablename__ = "scenario_categories"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    course_id: Optional[uuid.UUID] = Field(default=None, foreign_key="courses.id", index=True)
    name: str = Field(unique=True, index=True, max_length=100)  # slug
    title: str = Field(max_length=200)
    description: str = Field(max_length=500)
    icon_name: str = Field(max_length=100)
    order_index: int = Field(default=0)
    translations: Optional[dict] = Field(default=None, sa_column=Column(JSONB))


class Scenario(SQLModel, table=True):
    __tablename__ = "scenarios"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    category_id: uuid.UUID = Field(foreign_key="scenario_categories.id", index=True)
    title: str = Field(max_length=200)
    description: str = Field(sa_column=Column(Text))
    mode: PracticeMode
    system_prompt: str = Field(sa_column=Column(Text))
    difficulty: Difficulty
    tags: Optional[list] = Field(default=[], sa_column=Column(JSONB))
    order_index: int = Field(default=0)
    is_active: bool = Field(default=True)
    translations: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
