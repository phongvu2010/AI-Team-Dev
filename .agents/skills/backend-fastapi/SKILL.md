---
name: backend-fastapi
description: >-
  Python FastAPI, Pydantic v2, and layered service architecture patterns for the Backend Dev Team (backend-dev). Activate when building REST API endpoints, Pydantic v2 validation schemas, dependency injection, or async business logic in src/backend/.
---

# Backend Team Runbook: FastAPI + Pydantic v2 + Async Services

Runbook này hướng dẫn `backend-dev` xây dựng REST API chất lượng cao, tuân thủ nghiêm ngặt **Cross-Layer Data Contract Matrix**, rào chắn an toàn dòng lệnh (**CLI Guardrails**) và tham gia vòng lặp tự sửa lỗi (**Feedback Loop**).

---

## 1. Rào Chắn An Toàn Dòng Lệnh (CLI Guardrails)
- **Quyền sở hữu**: Chỉ tạo/sửa file trong `src/backend/`.
- **Lệnh được phép**:
  - `.venv/bin/ruff check src/backend/`
  - `python3 -m py_compile src/backend/...`
- **Lệnh cấm**: Cấm chạy `pip install` trần trong sandbox; cấm sửa file ngoài `src/backend/`; cấm gọi `pytest`/`ruff` trần của hệ thống.

---

## 2. Cấu Trúc Thư Mục Chuẩn (`src/backend/`)

```text
src/backend/
├── app/
│   ├── __init__.py
│   ├── main.py               # Khởi tạo FastAPI app, CORS, Lifespan, Exception Handlers
│   ├── core/                 # Cấu hình (config.py), bảo mật (security.py), lỗi chuẩn
│   ├── schemas/              # Pydantic v2 Schemas (Create, Update, Response)
│   ├── services/             # Business Logic & Transaction Management
│   └── api/
│       └── v1/
│           ├── router.py     # Gộp các APIRouter
│           └── endpoints/    # Từng nhóm route theo resource
└── tests/                    # Bộ kiểm thử pytest + httpx.AsyncClient
    ├── conftest.py           # Test fixtures + SQLite async in-memory fallback
    └── test_api_*.py
```

---

## 3. Quy Chuẩn Đồng Bộ Hợp Đồng (Contract Synchronization)

1. **Thống nhất Casing `snake_case`**:
   - Mọi thuộc tính của Pydantic schema và JSON response của REST API thống nhất sử dụng chuẩn **`snake_case`**. Tên trường phải khớp 100% với mục Cross-Layer Data Contract Matrix trong `docs/specs/<feature-slug>/plan.md`.
2. **Pydantic v2 Schema Mẫu**:
   ```python
   from datetime import datetime
   from uuid import UUID
   from pydantic import BaseModel, ConfigDict, Field


   class ItemCreate(BaseModel):
       title: str = Field(..., min_length=1, max_length=255, description="Tiêu đề tài nguyên")
       description: str | None = Field(default=None, max_length=2000, description="Mô tả chi tiết")
       tags: list[str] = Field(default_factory=list, description="Danh sách nhãn")


   class ItemUpdate(BaseModel):
       title: str | None = Field(default=None, min_length=1, max_length=255)
       description: str | None = Field(default=None, max_length=2000)
       tags: list[str] | None = None


   class ItemResponse(BaseModel):
       model_config = ConfigDict(from_attributes=True)

       id: UUID
       title: str
       description: str | None
       tags: list[str]
       created_at: datetime
       updated_at: datetime
   ```
3. **Chuẩn hóa Phản hồi Lỗi (Standard Error Handling)**:
   - Sử dụng `HTTPException(status_code=..., detail="Mô tả lỗi")` nhất quán với API Contract.
   - Không để lộ thông tin nhạy cảm hoặc exception traceback nội bộ ra ngoài client.

---

## 4. Kết Nối Database & Dependency Injection
- Dự án cấu hình `pythonpath = ["src"]` trong `pyproject.toml`, do đó import trực tiếp từ `db`:
  ```python
  from db.models.item import Item
  from db.session import get_db_session
  from db.repositories.item_repository import get_item_by_id
  ```
- Sử dụng `Annotated[AsyncSession, Depends(get_db_session)]` cho DI gọn gàng, rõ kiểu.
- Endpoint POST trả về `status_code=status.HTTP_201_CREATED`, DELETE trả về `status_code=status.HTTP_204_NO_CONTENT`.

---

## 5. Tham Gia Vòng Lặp Sửa Lỗi (Feedback Loop Protocol)
Khi nhận tin nhắn `[SELF-HEALING ACTION REQUIRED]` từ QA hoặc `[REVIEW-FIX ACTION REQUIRED]` từ Reviewer:
1. Xác định lỗi từ file, dòng code và traceback được cung cấp.
2. Sửa lỗi trong `src/backend/`, chạy smoke test: `.venv/bin/ruff check src/backend/` và `python3 -m py_compile src/backend/...`.
3. Phản hồi cho Tech Lead bằng thông điệp `[FIX-COMPLETED]`:
   ```text
   [FIX-COMPLETED]
   - Feature: <feature-slug>
   - Iteration: <iteration_number>
   - Target Agent: backend-dev
   - Modified Files: <danh sách files đã sửa>
   - Contract Modified: TRUE | FALSE
   - Contract Changes: <chi tiết thay đổi schema/endpoint nếu TRUE, hoặc NONE>
   - Resolved Bug/Finding IDs: <BUG-01, ...>
   - Summary of Fix: <tóm tắt ngắn gọn giải pháp>
   ```
