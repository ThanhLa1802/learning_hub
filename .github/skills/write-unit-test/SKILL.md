---
name: write-unit-test
description: 'Write unit or integration tests for the backend. Use when testing FastAPI endpoints, repositories, or services. Covers pytest setup, SQLite in-memory DB for repos, TestClient for endpoints, and mocking OpenAI.'
argument-hint: 'Describe what to test (e.g. "test lesson repository" or "test POST /lessons endpoint")'
---

# Write Unit Tests

## Stack

- `pytest` — test runner
- `httpx` + `fastapi.testclient.TestClient` — endpoint (integration) tests
- `sqlmodel` với SQLite in-memory — repo tests (không cần Postgres thật)
- `unittest.mock.patch` — mock OpenAI calls trong service tests

## Cài đặt (chỉ làm một lần)

```bash
pip install pytest pytest-asyncio httpx
```

Thêm vào `backend/requirements.txt`:
```
pytest
pytest-asyncio
httpx
```

## Cấu trúc thư mục

```
backend/
  tests/
    __init__.py
    conftest.py          ← shared fixtures (session, client, test user)
    test_repositories/
      __init__.py
      test_lesson.py
    test_endpoints/
      __init__.py
      test_lessons.py
    test_services/
      __init__.py
      test_lesson_service.py
```

## conftest.py — Fixtures dùng chung

```python
# backend/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.core.database import get_session
from app.models.user import User
from app.core.security import create_access_token

# ── SQLite in-memory engine (dùng cho tất cả tests) ──────────────────────────
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

# ── Override DB dependency cho endpoint tests ─────────────────────────────────
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# ── Test user fixtures ────────────────────────────────────────────────────────
@pytest.fixture(name="test_user")
def test_user_fixture(session: Session) -> User:
    from app.core.security import get_password_hash
    user = User(email="test@example.com", hashed_password=get_password_hash("password"))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture(name="admin_user")
def admin_user_fixture(session: Session) -> User:
    from app.core.security import get_password_hash
    user = User(email="admin@example.com", hashed_password=get_password_hash("password"), is_admin=True)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture(name="auth_cookies")
def auth_cookies_fixture(test_user: User) -> dict:
    """Return cookie dict để truyền vào client.get(..., cookies=auth_cookies)"""
    from app.core.security import create_access_token
    token = create_access_token({"sub": str(test_user.id), "type": "access"})
    return {"access_token": token}

@pytest.fixture(name="admin_cookies")
def admin_cookies_fixture(admin_user: User) -> dict:
    from app.core.security import create_access_token
    token = create_access_token({"sub": str(admin_user.id), "type": "access"})
    return {"access_token": token}
```

## Repository Tests (unit, dùng SQLite session)

Pattern thực tế cho `backend/app/repositories/lesson.py`:

```python
# backend/tests/test_repositories/test_lesson.py
import uuid
import pytest
from sqlmodel import Session
from app.repositories import lesson as lesson_crud
from app.models.lesson import Lesson
from app.models.domain import Domain, Course

def make_course(session: Session) -> Course:
    domain = Domain(slug="test", name="Test", description="d", icon_name="x", color="blue", order_index=0)
    session.add(domain)
    session.commit()
    course = Course(domain_id=domain.id, slug="c1", name="Course", description="d", order_index=0)
    session.add(course)
    session.commit()
    return course

def test_get_by_id_returns_lesson(session: Session):
    course = make_course(session)
    lesson = Lesson(course_id=course.id, title="Hello", content="World", order_index=0)
    session.add(lesson)
    session.commit()

    result = lesson_crud.get_by_id(session, lesson.id)

    assert result is not None
    assert result.title == "Hello"

def test_get_by_id_returns_none_for_unknown(session: Session):
    result = lesson_crud.get_by_id(session, uuid.uuid4())
    assert result is None

def test_get_by_course_returns_active_only(session: Session):
    course = make_course(session)
    active = Lesson(course_id=course.id, title="Active", content="x", order_index=0, is_active=True)
    inactive = Lesson(course_id=course.id, title="Inactive", content="x", order_index=1, is_active=False)
    session.add_all([active, inactive])
    session.commit()

    results = lesson_crud.get_by_course(session, course.id)

    assert len(results) == 1
    assert results[0].title == "Active"

def test_mark_complete_is_idempotent(session: Session):
    course = make_course(session)
    lesson = Lesson(course_id=course.id, title="L", content="c", order_index=0)
    session.add(lesson)
    session.commit()
    user_id = uuid.uuid4()

    p1 = lesson_crud.mark_complete(session, user_id, lesson.id)
    p2 = lesson_crud.mark_complete(session, user_id, lesson.id)

    assert p1.id == p2.id  # không tạo duplicate
```

## Endpoint Tests (integration, dùng TestClient)

Auth được truyền qua cookie (project dùng cookie-based auth):

```python
# backend/tests/test_endpoints/test_lessons.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models.lesson import Lesson
from app.models.domain import Domain, Course

def make_lesson(session: Session) -> Lesson:
    domain = Domain(slug="eng", name="English", description="d", icon_name="x", color="blue", order_index=0)
    session.add(domain)
    session.commit()
    course = Course(domain_id=domain.id, slug="c1", name="C1", description="d", order_index=0)
    session.add(course)
    session.commit()
    lesson = Lesson(course_id=course.id, title="Test Lesson", content="Content here", order_index=0)
    session.add(lesson)
    session.commit()
    return lesson

def test_get_lesson_requires_auth(client: TestClient, session: Session):
    lesson = make_lesson(session)
    r = client.get(f"/api/v1/lessons/{lesson.id}")
    assert r.status_code == 401

def test_get_lesson_returns_data(client: TestClient, session: Session, auth_cookies: dict):
    lesson = make_lesson(session)
    r = client.get(f"/api/v1/lessons/{lesson.id}", cookies=auth_cookies)
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Test Lesson"
    assert data["content"] == "Content here"

def test_get_lesson_not_found(client: TestClient, auth_cookies: dict):
    import uuid
    r = client.get(f"/api/v1/lessons/{uuid.uuid4()}", cookies=auth_cookies)
    assert r.status_code == 404

def test_admin_list_lessons_requires_admin(client: TestClient, auth_cookies: dict):
    r = client.get("/api/v1/admin/lessons", cookies=auth_cookies)
    assert r.status_code == 403  # user thường bị từ chối

def test_admin_list_lessons_ok(client: TestClient, admin_cookies: dict):
    r = client.get("/api/v1/admin/lessons", cookies=admin_cookies)
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    assert "total" in data
```

## Service Tests (mock OpenAI)

```python
# backend/tests/test_services/test_lesson_service.py
from unittest.mock import MagicMock, patch

def test_explain_lesson_calls_openai():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = '{"explanation": "test", "key_points": [], "real_world_example": "ex", "interview_tip": "tip"}'

    with patch("app.services.lesson_service.client.chat.completions.create", return_value=mock_response):
        from app.services import lesson_service
        result = lesson_service.explain_lesson("What is a REST API?", "Lesson content")

    assert result["explanation"] == "test"
    assert isinstance(result["key_points"], list)

def test_explain_lesson_returns_correct_schema():
    mock_content = {
        "explanation": "REST is...",
        "key_points": ["stateless", "HTTP methods"],
        "real_world_example": "GitHub API",
        "interview_tip": "Mention HTTP verbs"
    }
    import json
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps(mock_content)

    with patch("app.services.lesson_service.client.chat.completions.create", return_value=mock_response):
        from app.services import lesson_service
        result = lesson_service.explain_lesson("q", "content")

    # Verify tất cả keys mà frontend expect
    assert "explanation" in result
    assert "key_points" in result
    assert "real_world_example" in result
    assert "interview_tip" in result
```

## Chạy tests

```bash
# Từ thư mục backend/
pytest tests/ -v

# Chỉ chạy 1 file
pytest tests/test_repositories/test_lesson.py -v

# Chỉ chạy 1 test case
pytest tests/test_endpoints/test_lessons.py::test_get_lesson_returns_data -v

# Xem coverage
pytest tests/ --cov=app --cov-report=term-missing
```

## Checklist

- [ ] `conftest.py` có đủ fixtures: `session`, `client`, `auth_cookies`, `admin_cookies`
- [ ] Repo tests dùng `session` fixture (SQLite), KHÔNG dùng `client`
- [ ] Endpoint tests dùng `client` fixture, truyền cookie qua `cookies=auth_cookies`
- [ ] Admin endpoints được test cả 403 (user thường) lẫn 200 (admin)
- [ ] OpenAI calls được mock bằng `patch`, không gọi API thật
- [ ] Mỗi test function chỉ assert một behavior cụ thể
- [ ] Helper factories (như `make_lesson`) đặt trong file test hoặc `conftest.py` nếu dùng chung

## Lưu ý

- **Không** commit file `.env` hay API key vào test
- Test fixtures tạo data mới mỗi lần → tests độc lập, không phụ thuộc thứ tự chạy
- SQLite không hỗ trợ JSONB → test liên quan đến `translations` cần dùng Postgres thật hoặc mock ở tầng repo
