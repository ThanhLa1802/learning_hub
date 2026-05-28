import uuid

from pydantic import BaseModel, ConfigDict


class DomainResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    name: str
    description: str
    icon_name: str
    color: str
    order_index: int


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    domain_id: uuid.UUID
    slug: str
    name: str
    description: str
    order_index: int


class DomainWithCoursesResponse(DomainResponse):
    courses: list[CourseResponse] = []
