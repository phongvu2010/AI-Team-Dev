# Backend Layer Rules (`src/backend/AGENTS.md`)

Quy tắc bắt buộc khi bất kỳ Agent nào (`backend-dev`, `qa-tester`, `code-reviewer`) thao tác trong thư mục `src/backend/`:

---

## 1. Rào Chắn An Toàn Dòng Lệnh & Phân Quyền (CLI Guardrails)
- **Quyền sở hữu File**: Tác tử `backend-dev` chỉ được tạo và chỉnh sửa file trong `src/backend/`. Tuyệt đối không can thiệp vào `src/db/` hay `src/frontend/`.
- **Lệnh được phép (Đa nền tảng)**:
  - *Windows*: `.\.venv\Scripts\python.exe -m ruff check src/backend/` (hoặc `python -m ruff check src/backend/`), `python -m py_compile src/backend/...`
  - *Linux / macOS*: `.venv/bin/python -m ruff check src/backend/`, `python3 -m py_compile src/backend/...`
- **Lệnh cấm tuyệt đối**:
  - Cấm `rm -rf`, `dropdb`, `git reset`, `git checkout`.
  - Cấm tự ý sửa `pyproject.toml`, `docker-compose.yml`, `alembic.ini`. Cấm chạy `pip install` trần trong sandbox. Khi cần thêm thư viện Python mới, BẮT BUỘC chỉ cắm cờ `[DEPENDENCY REQUIRED]` để Tech Lead Orchestrator trực tiếp cập nhật.
  - Cấm gọi lệnh `pytest`, `ruff`, `python` trần không rõ virtualenv.

---

## 2. Tuân Thủ Hợp Đồng API & Dữ Liệu Xuyên Tầng (Contract Alignment)
- Đường dẫn URL, HTTP Method, Query Params, Request/Response JSON và HTTP Status Code phải khớp 100% với mục **Cross-Layer Data Contract Matrix** và **API Contract** trong `docs/specs/<feature-slug>/plan.md`.
- **Casing**: REST API payloads và Pydantic schemas sử dụng thống nhất chuẩn **`snake_case`**. Tên trường JSON trả về cho Frontend phải khớp 1:1, không dùng mapping ngầm gây lỗi undefined.
- **Pydantic v2 Chuẩn hóa**:
  - Luôn sử dụng `BaseModel`, `Field`, `ConfigDict(from_attributes=True)`.
  - Dùng `.model_dump()` và `.model_validate()`, không dùng cú pháp Pydantic v1 cũ (`.dict()`, `orm_mode = True`).
  - Ràng buộc chặt chẽ độ dài chuỗi (`min_length`, `max_length`), khoảng giá trị số (`ge`, `le`) để chống tràn bộ nhớ và tấn công DoS.
- **Chuẩn hóa Error Responses**:
  - Mọi lỗi nghiệp vụ phải trả về `HTTPException(status_code=..., detail="...")` nhất quán với mã lỗi và schema trong `plan.md`.
  - Tuyệt đối không để lộ raw exception traceback hoặc thông tin nhạy cảm (database credentials, secrets) ra client.

---

## 3. Kiến Trúc Phân Lớp & Import Convention
- `app/core/config.py`: Quản lý cấu hình tập trung (`settings = Settings()`, kế thừa `BaseSettings`).
- `app/schemas/`: Định nghĩa Pydantic v2 schemas theo tài nguyên.
- `app/services/`: Xử lý business logic và transaction (`commit` / `rollback`).
- `app/api/v1/endpoints/`: Khai báo FastAPI `APIRouter`, `Depends`, `status_code` và `response_model`.
- `app/api/v1/router.py`: Cắm các router con vào router tập trung tại `/api/v1`.
- **Import từ DB Layer**: Do dự án đã có cấu hình `pythonpath = ["src"]`, bạn import trực tiếp từ `db`:
  ```python
  from db.models.item import Item
  from db.session import get_db_session
  from db.repositories.item_repository import get_item_by_id
  ```

---

## 4. Tham Gia Vòng Lặp Sửa Lỗi (Feedback Loop Protocol)
Khi nhận tin nhắn điều phối `[SELF-HEALING ACTION REQUIRED]` từ QA hoặc `[REVIEW-FIX ACTION REQUIRED]` từ Reviewer:
1. Phân tích nguyên nhân và **chỉ chỉnh sửa trong phạm vi `src/backend/`**.
2. Kiểm tra smoke check: `python -m ruff check src/backend/` và `python -m py_compile src/backend/...`.
3. Gửi thông điệp phản hồi `[FIX-COMPLETED]` cho Tech Lead Orchestrator:
   ```text
   [FIX-COMPLETED]
   - Feature: <feature-slug>
   - Iteration: <iteration_number>
   - Target Agent: backend-dev
   - Modified Files: src/backend/...
   - Contract Modified: TRUE | FALSE
   - Contract Changes: <chi tiết thay đổi schema/endpoint nếu TRUE, hoặc NONE>
   - Resolved Bug/Finding IDs: <BUG-01 hoặc REV-01>
   - Summary of Fix: <tóm tắt ngắn giải pháp đã thực hiện>
   ```
