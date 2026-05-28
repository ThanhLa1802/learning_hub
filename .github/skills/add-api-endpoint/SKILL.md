---
name: add-api-endpoint
description: 'Add a new FastAPI endpoint to the backend. Use when creating new API routes, new resource types, or new backend features. Covers model, schema, repository, service, endpoint, and router registration.'
argument-hint: 'Describe the new endpoint (e.g. "GET /tags to list all tags")'
---

# Add API Endpoint

## Quy trình chuẩn (theo thứ tự)

### 1. Model — `backend/app/models/<resource>.py`
- Kế thừa `SQLModel, table=True`
- Dùng `uuid.UUID` làm primary key với `default_factory=uuid.uuid4`
- Thêm `translations: dict = Field(default={}, sa_column=Column(JSONB))` nếu cần đa ngôn ngữ
- Đăng ký import trong `backend/app/models/__init__.py`

### 2. Schema — `backend/app/schemas/<resource>.py`
- `BaseModel` với `ConfigDict(from_attributes=True)` cho response schemas
- Tách `CreateRequest`, `UpdateRequest`, `Response` rõ ràng
- Đăng ký trong `backend/app/schemas/__init__.py`

### 3. Repository — `backend/app/repositories/<resource>.py`
- Nhận `Session` từ SQLModel làm tham số đầu tiên
- Chỉ chứa DB queries thuần (select, insert, update, delete)
- Không chứa business logic
- Đăng ký trong `backend/app/repositories/__init__.py`

### 4. Service (nếu cần AI hoặc logic phức tạp) — `backend/app/services/<resource>_service.py`
- Gọi OpenAI với `response_format={"type": "json_object"}` nếu dùng AI
- Trả về typed Python objects, không trả raw JSON string

### 5. Endpoint — `backend/app/api/v1/endpoints/<resource>.py`
- Route mỏng: chỉ validate input → gọi repository/service → trả response
- Dùng `SessionDep` và `CurrentUser` từ `app.api.v1.deps`
- Gọi `apply_lang(obj, lang)` nếu endpoint hỗ trợ `lang` query param
- Không nhúng business logic vào route

```python
from fastapi import APIRouter
from app.api.v1.deps import CurrentUser, SessionDep
from app.repositories import <resource> as <resource>_crud
from app.schemas.<resource> import <Resource>Response

router = APIRouter()

@router.get("/", response_model=list[<Resource>Response])
def list_<resource>s(session: SessionDep, _: CurrentUser):
    return <resource>_crud.get_all(session)
```

### 6. Router — `backend/app/api/v1/router.py`
```python
from app.api.v1.endpoints import <resource>
router.include_router(<resource>.router, prefix="/<resource>s", tags=["<resource>s"])
```

## Checklist

- [ ] Model định nghĩa đúng kiểu dữ liệu, có `table=True`
- [ ] Schema Response dùng `from_attributes=True`
- [ ] Repository không có business logic
- [ ] Route không có DB query trực tiếp
- [ ] Protected route dùng `CurrentUser` dep
- [ ] Admin route dùng `require_admin` dep
- [ ] `apply_lang` được gọi nếu model có `translations`
- [ ] Import đăng ký trong `__init__.py` tương ứng
- [ ] Router đã `include_router` trong `router.py`

## Lưu ý bảo mật
- Admin endpoints PHẢI có `require_admin` dependency — không bỏ qua
- Không lộ thông tin nội bộ trong error messages (dùng HTTPException với message chung)
- Validate UUID params qua type annotation, không dùng string raw
