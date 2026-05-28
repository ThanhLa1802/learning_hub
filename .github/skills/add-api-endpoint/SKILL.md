---
name: add-api-endpoint
description: 'Add a new FastAPI endpoint to the backend. Use when creating new API routes, new resource types, or new backend features. Covers model, schema, repository, service, endpoint, and router registration.'
argument-hint: 'Describe the new endpoint (e.g. "GET /tags to list all tags")'
---

# Add API Endpoint

## Quy trình chuẩn (theo thứ tự)

### 1. Model — `backend/app/models/<resource>.py`

Pattern thực tế từ `backend/app/models/lesson.py`:

```python
import uuid
from typing import Optional
from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

class Lesson(SQLModel, table=True):
    __tablename__ = "lessons"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    course_id: uuid.UUID = Field(foreign_key="courses.id", index=True)
    title: str = Field(max_length=200)
    content: str = Field(sa_column=Column(Text))          # dùng Text cho chuỗi dài
    order_index: int = Field(default=0)
    is_active: bool = Field(default=True)
    translations: Optional[dict] = Field(default=None, sa_column=Column(JSONB))  # đa ngôn ngữ
```

- Luôn dùng `uuid.UUID` làm primary key với `default_factory=uuid.uuid4`
- Dùng `Column(Text)` cho nội dung dài, `Column(JSONB)` cho dict/translations
- Đăng ký import trong `backend/app/models/__init__.py`

### 2. Schema — `backend/app/schemas/<resource>.py`

Pattern thực tế từ `backend/app/schemas/lesson.py`:

```python
import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict

class LessonSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)   # bắt buộc cho response schemas
    id: uuid.UUID
    title: str
    order_index: int
    is_completed: bool = False          # field tính toán, không có trong model

class LessonResponse(LessonSummaryResponse):          # kế thừa để tránh lặp
    course_id: uuid.UUID
    content: str
    next_lesson_id: Optional[uuid.UUID] = None

class LessonCreate(BaseModel):                        # input schema không cần from_attributes
    course_id: uuid.UUID
    title: str
    content: str

class LessonUpdate(BaseModel):                        # tất cả Optional cho PATCH-style update
    title: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None
```

- Response schemas PHẢI có `ConfigDict(from_attributes=True)`
- Update schemas dùng `Optional` cho tất cả fields + `body.model_dump(exclude_none=True)` khi apply
- Đăng ký trong `backend/app/schemas/__init__.py`

### 3. Repository — `backend/app/repositories/<resource>.py`

Pattern thực tế từ `backend/app/repositories/lesson.py`:

```python
import uuid
from typing import Optional
from sqlmodel import Session, select
from app.models.lesson import Lesson

def get_by_id(session: Session, lesson_id: uuid.UUID) -> Optional[Lesson]:
    return session.get(Lesson, lesson_id)

def get_by_course(session: Session, course_id: uuid.UUID) -> list[Lesson]:
    return list(session.exec(
        select(Lesson)
        .where(Lesson.course_id == course_id, Lesson.is_active == True)
        .order_by(Lesson.order_index)
    ).all())

def create(session: Session, data: dict) -> Lesson:
    obj = Lesson(**data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, obj: Lesson, updates: dict) -> Lesson:
    for field, value in updates.items():
        setattr(obj, field, value)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj
```

- Nhận `Session` (không phải `SessionDep`) làm tham số đầu tiên
- Chỉ chứa DB queries — **không** có HTTPException, business logic hay AI calls
- Đăng ký trong `backend/app/repositories/__init__.py`

### 4. Service (chỉ khi cần AI hoặc logic phức tạp)

```python
# backend/app/services/<resource>_service.py
from openai import OpenAI
client = OpenAI()

def generate_something(prompt: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},   # luôn dùng json_object cho AI flows
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)
```

### 5. Endpoint — `backend/app/api/v1/endpoints/<resource>.py`

Pattern thực tế từ `backend/app/api/v1/endpoints/lessons.py`:

```python
import uuid
from fastapi import APIRouter, HTTPException, status
from app.api.v1.deps import CurrentUser, SessionDep
from app.repositories import lesson as lesson_crud
from app.schemas.lesson import LessonResponse, LessonUpdate
from app.utils.translation import apply_lang

router = APIRouter()

@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: uuid.UUID, session: SessionDep, current_user: CurrentUser, lang: str = "en"):
    lesson = lesson_crud.get_by_id(session, lesson_id)
    if not lesson or not lesson.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    response = LessonResponse.model_validate(lesson)
    apply_lang(response, lesson.translations, lang)   # gọi nếu model có translations
    return response

@router.put("/{lesson_id}", response_model=LessonResponse)
def update_lesson(lesson_id: uuid.UUID, body: LessonUpdate, session: SessionDep, _: CurrentUser):
    lesson = lesson_crud.get_by_id(session, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson_crud.update(session, lesson, body.model_dump(exclude_none=True))
```

**Admin endpoint pattern** — từ `backend/app/api/v1/endpoints/admin.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.v1.deps import CurrentUser, SessionDep
from app.models.user import User

router = APIRouter()

def require_admin(current_user: CurrentUser) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user

AdminDep = Depends(require_admin)

@router.get("/items", response_model=list[ItemResponse])
def list_items(session: SessionDep, _: User = AdminDep):
    ...
```

### 6. Router — `backend/app/api/v1/router.py`

Thêm vào cuối file, theo pattern hiện có:

```python
from app.api.v1.endpoints import <resource>
router.include_router(<resource>.router, prefix="/<resource>s", tags=["<resource>s"])
```

## Checklist

- [ ] Model có `table=True`, primary key UUID với `default_factory`
- [ ] Schema Response có `ConfigDict(from_attributes=True)`
- [ ] Schema Update dùng `Optional` cho tất cả fields
- [ ] Repository chỉ có DB queries, nhận `Session` không phải `SessionDep`
- [ ] Endpoint dùng `model_dump(exclude_none=True)` khi update
- [ ] Protected route dùng `CurrentUser` dep
- [ ] Admin route dùng `AdminDep = Depends(require_admin)` — **không bỏ qua**
- [ ] Endpoint gọi `apply_lang(response, obj.translations, lang)` nếu model có `translations`
- [ ] Import đăng ký trong `__init__.py` của models, schemas, repositories
- [ ] `router.include_router(...)` đã thêm vào `backend/app/api/v1/router.py`

## Lưu ý bảo mật
- Admin endpoints PHẢI có `require_admin` — không bỏ qua dù chỉ là GET
- Không lộ thông tin nội bộ trong error messages (dùng HTTPException với message chung)
- UUID params validate qua type annotation `uuid.UUID`, không dùng `str` raw
