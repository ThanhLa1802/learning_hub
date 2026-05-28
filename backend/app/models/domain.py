import uuid
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class Domain(SQLModel, table=True):
    __tablename__ = "domains"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    slug: str = Field(unique=True, index=True, max_length=100)
    name: str = Field(max_length=200)
    description: str = Field(max_length=500)
    icon_name: str = Field(max_length=100)
    color: str = Field(max_length=50, default="blue")  # tailwind color name
    order_index: int = Field(default=0)
    is_active: bool = Field(default=True)
    translations: Optional[dict] = Field(default=None, sa_column=Column(JSONB))


class Course(SQLModel, table=True):
    __tablename__ = "courses"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    domain_id: uuid.UUID = Field(foreign_key="domains.id", index=True)
    slug: str = Field(unique=True, index=True, max_length=100)
    name: str = Field(max_length=200)
    description: str = Field(max_length=500)
    order_index: int = Field(default=0)
    is_active: bool = Field(default=True)
    translations: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
