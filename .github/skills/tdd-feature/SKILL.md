---
name: tdd-feature
description: 'Develop a new backend feature using Test-Driven Development (TDD). Use when adding a new repository function, endpoint, or service — write failing tests first, then implement until they pass. Covers the full Red → Green → Refactor cycle for this codebase.'
argument-hint: 'Describe the feature (e.g. "add get_by_tag to scenario repository" or "POST /tags endpoint")'
---

# Test-Driven Development — New Feature

## TDD Cycle for This Codebase

```
RED   → Write a failing test that describes the expected behavior
GREEN → Write the minimum implementation to make it pass
REFACTOR → Clean up without breaking tests
```

Work in this exact order. Never write implementation before the test.

---

## Step 1 — Identify the layer

| Layer | Test file | Implementation file |
|---|---|---|
| Repository | `backend/tests/test_repositories/test_<resource>.py` | `backend/app/repositories/<resource>.py` |
| Endpoint | `backend/tests/test_endpoints/test_<resource>.py` | `backend/app/api/v1/endpoints/<resource>.py` |
| Service | `backend/tests/test_services/test_<resource>_service.py` | `backend/app/services/<resource>_service.py` |

---

## Step 2 — RED: Write the failing test

### Repository test (SQLite in-memory)

```python
# backend/tests/test_repositories/test_<resource>.py
import uuid
import pytest
from sqlmodel import Session
from app.repositories import <resource> as <resource>_crud
from app.models.<resource> import <Resource>

def test_<function>_<expected_behavior>(session: Session):
    # Arrange — insert minimum required data
    obj = <Resource>(field="value", ...)
    session.add(obj)
    session.commit()

    # Act
    result = <resource>_crud.<function>(session, obj.id)

    # Assert — one behavior per test
    assert result is not None
    assert result.field == "value"
```

**Key rules:**
- One `assert` target per test (single behavior)
- Helper factories (`make_<resource>`) at module top, not inside tests
- Use `uuid.uuid4().hex[:6]` suffix on slugs/names to avoid unique-constraint collisions across tests
- Fixtures come from `tests/conftest.py`: `session`, `client`, `auth_cookies`, `admin_cookies`

### Endpoint test (TestClient + cookies)

```python
# backend/tests/test_endpoints/test_<resource>.py
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models.<resource> import <Resource>

def test_<endpoint>_requires_auth(client: TestClient):
    r = client.get("/api/v1/<resource>/")
    assert r.status_code == 401

def test_<endpoint>_returns_data(client: TestClient, session: Session, auth_cookies: dict):
    # Arrange
    obj = <Resource>(...)
    session.add(obj); session.commit()

    # Act
    r = client.get(f"/api/v1/<resource>/{obj.id}", cookies=auth_cookies)

    # Assert
    assert r.status_code == 200
    assert r.json()["field"] == "expected"

def test_<endpoint>_not_found(client: TestClient, auth_cookies: dict):
    r = client.get(f"/api/v1/<resource>/{uuid.uuid4()}", cookies=auth_cookies)
    assert r.status_code == 404
```

**Key rules:**
- Always test the unauthenticated case (`401`) first
- Admin endpoints: test `403` with `auth_cookies`, `200` with `admin_cookies`
- Extract error detail as `r.json()["detail"]`, not a message field

### Service test (mock OpenAI)

```python
# backend/tests/test_services/test_<resource>_service.py
import json
from unittest.mock import MagicMock, patch

def test_<function>_returns_correct_schema():
    mock_content = {"key": "value", ...}
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps(mock_content)

    with patch("app.services.<resource>_service.client.chat.completions.create",
               return_value=mock_response):
        from app.services import <resource>_service
        result = <resource>_service.<function>("input")

    assert result["key"] == "value"
```

---

## Step 3 — Run tests, confirm RED

```bash
# From backend/
pytest tests/test_repositories/test_<resource>.py::test_<function>_<behavior> -v
```

Expected: `FAILED` with `ImportError` or `AttributeError` (function doesn't exist yet). If the test passes immediately, the test is wrong — revise it.

---

## Step 4 — GREEN: Write minimum implementation

### Repository function

```python
# backend/app/repositories/<resource>.py
from sqlmodel import Session, select
from app.models.<resource> import <Resource>

def <function>(session: Session, id: uuid.UUID) -> Optional[<Resource>]:
    return session.get(<Resource>, id)            # PK lookup
    # OR for filtered queries:
    return list(session.exec(
        select(<Resource>).where(<Resource>.field == value)
    ).all())
```

**Rules (non-negotiable):**
- Module-level functions only, no classes
- First param is `Session`, never `SessionDep`
- No `HTTPException`, no business logic
- PK lookup → `session.get(Model, id)`
- Filtered list → `select(...).where(...)`, wrap in `list(...)`
- Write: `session.add(obj)` → `session.commit()` → `session.refresh(obj)` → `return obj`

### Endpoint (after repository passes)

```python
# backend/app/api/v1/endpoints/<resource>.py
from fastapi import APIRouter, HTTPException
from app.api.v1.deps import SessionDep, CurrentUser
from app.repositories import <resource> as <resource>_crud
from app.schemas.<resource> import <Resource>Response
from app.utils.translation import apply_lang

router = APIRouter()

@router.get("/{id}", response_model=<Resource>Response)
def get_<resource>(id: uuid.UUID, lang: str = "en",
                   session: SessionDep = ..., _: CurrentUser = ...):
    obj = <resource>_crud.get_by_id(session, id)
    if not obj or not obj.is_active:
        raise HTTPException(404, detail="Not found")
    response = <Resource>Response.model_validate(obj)
    # set computed fields here, e.g. response.is_completed = ...
    apply_lang(response, obj.translations, lang)
    return response
```

**Rules:**
- Import repo with `_crud` alias
- `model_validate(obj)` — not `from_orm`
- Set computed fields on `response` **after** `model_validate`, **before** `apply_lang`
- `apply_lang` on the response schema instance, not on `obj`
- Register in `backend/app/api/v1/router.py`

---

## Step 5 — Run tests, confirm GREEN

```bash
pytest tests/test_repositories/test_<resource>.py -v
pytest tests/test_endpoints/test_<resource>.py -v
```

All targeted tests should pass. If not, fix only the implementation — do not weaken the test.

---

## Step 6 — REFACTOR

Only after GREEN:
- Extract repeated setup into a `make_<resource>` factory if used in 3+ tests
- Remove duplication in implementation
- Run tests again to confirm nothing broke

```bash
pytest tests/ -v
```

---

## Checklist

- [ ] Test written and confirmed **FAILED** before any implementation
- [ ] One behavior asserted per test function
- [ ] Helper factories use random suffixes to avoid unique-constraint conflicts
- [ ] Repository: no `HTTPException`, no business logic
- [ ] Endpoint: `model_validate` → computed fields → `apply_lang` → return
- [ ] Admin routes: `AdminDep` added manually, tested for both 403 and 200
- [ ] New model/schema/repo files added to their `__init__.py`
- [ ] New endpoint registered in `router.py`
- [ ] All existing tests still pass after refactor

## SQLite caveat

`translations` (JSONB) tests run on SQLite because `conftest.py` patches `visit_JSONB → JSON`. Tests that assert on **translated content** (i.e., call `apply_lang`) should be endpoint-level tests where the full response object is available — not repo-level, which only returns raw models.
