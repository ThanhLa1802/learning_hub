import uuid
from typing import Optional

from pydantic import BaseModel


# ─── Domain ───────────────────────────────────────────────────────────────────

class DomainCreate(BaseModel):
    slug: str
    name: str
    description: str
    icon_name: str = "book-open"
    color: str = "blue"
    order_index: int = 0
    is_active: bool = True


class DomainUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon_name: Optional[str] = None
    color: Optional[str] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None


class DomainAdminResponse(BaseModel):
    id: uuid.UUID
    slug: str
    name: str
    description: str
    icon_name: str
    color: str
    order_index: int
    is_active: bool


# ─── Course ───────────────────────────────────────────────────────────────────

class CourseCreate(BaseModel):
    domain_id: uuid.UUID
    slug: str
    name: str
    description: str
    order_index: int = 0
    is_active: bool = True


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None


class CourseAdminResponse(BaseModel):
    id: uuid.UUID
    domain_id: uuid.UUID
    domain_name: str
    slug: str
    name: str
    description: str
    order_index: int
    is_active: bool


# ─── Lesson ───────────────────────────────────────────────────────────────────

class LessonCreate(BaseModel):
    course_id: uuid.UUID
    category_id: Optional[uuid.UUID] = None
    title: str
    content: str
    content_type: str = "explanation"
    order_index: int = 0
    estimated_minutes: int = 10
    is_active: bool = True


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[str] = None
    order_index: Optional[int] = None
    estimated_minutes: Optional[int] = None
    is_active: Optional[bool] = None
    category_id: Optional[uuid.UUID] = None


class LessonAdminResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    course_name: str
    domain_name: str
    title: str
    content_type: str
    order_index: int
    estimated_minutes: int
    is_active: bool
