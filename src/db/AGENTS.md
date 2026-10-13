# Database Layer Rules (`src/db/AGENTS.md`)

Quy tắc bắt buộc khi bất kỳ Agent nào (`db-dev`, `qa-tester`, `code-reviewer`) thao tác trong thư mục `src/db/`:

---

## 1. Rào Chắn An Toàn Dòng Lệnh & Phân Quyền (CLI Guardrails)
- **Quyền sở hữu File**: Tác tử `db-dev` chỉ được tạo và chỉnh sửa file trong `src/db/`. Tuyệt đối không can thiệp vào `src/backend/` hay `src/frontend/`.
- **Lệnh được phép (Đa nền tảng)**:
  - *Linux / macOS*: `.venv/bin/ruff check src/db/`, `.venv/bin/python src/db/seeds/runner.py`, `.venv/bin/python src/db/migrations/generate_offline_migration.py <slug>`, `alembic ...`
  - *Windows*: `python -m ruff check src/db/`, `python src/db/seeds/runner.py`, `python src/db/migrations/generate_offline_migration.py <slug>`, `alembic ...`
  - *Cú pháp chung*: `python -m py_compile src/db/...`
- **Lệnh cấm tuyệt đối**:
  - Cấm `rm -rf`, `dropdb`, `git reset`, `git checkout`.
  - Cấm tự ý sửa `pyproject.toml`, `docker-compose.yml`, `alembic.ini`. Cấm chạy `pip install` trần trong sandbox. Khi cần thêm thư viện mới, BẮT BUỘC chỉ cắm cờ `[DEPENDENCY REQUIRED]` để Tech Lead Orchestrator trực tiếp cập nhật.
  - Cấm gọi lệnh `pytest`, `ruff`, `python` trần không rõ virtualenv.

---

## 2. Tuân Thủ Hợp Đồng Dữ Liệu Xuyên Tầng (Contract Alignment)
- Tên bảng, tên cột và kiểu dữ liệu phải khớp 100% với mục **Cross-Layer Data Contract Matrix** trong `docs/specs/<feature-slug>/plan.md`.
- **Casing**: Toàn bộ tên cột và định danh bảng sử dụng chuẩn **`snake_case`**.
- **SQLAlchemy 2.0 Typing**: Bắt buộc dùng `DeclarativeBase`, `Mapped[...]` và `mapped_column(...)`. Không dùng `Column()` của SQLAlchemy 1.x.
- **Cross-DB Type Safety (SQLite Test Compatibility)**:
  - **UUID Khóa chính**: Sử dụng `from sqlalchemy import Uuid` kèm `default=uuid.uuid4` (hoặc kế thừa `UUIDPrimaryKeyMixin` từ `src/db/base.py`). Tuyệt đối không dùng `server_default=text("gen_random_uuid()")` hoặc kiểu dialect `UUID` trần.
  - **Mảng dữ liệu**: SQLite không hỗ trợ `ARRAY`. Dùng `from sqlalchemy import JSON` với `default=list` cho các mảng chuỗi (`list[str]`) hoặc variant `JSON().with_variant(ARRAY(String), "postgresql")`.
  - **JSON/JSONB**: Dùng `JSON` chuẩn hoặc variant với `JSONB`.
  - **Kiểu Dữ Liệu PostgreSQL Nâng Cao (Cross-DB Edge Cases)**:
    - Khi BẮT BUỘC dùng tính năng độc quyền PostgreSQL (`pgvector` Vector, `TSVECTOR` Full-Text Search, PostgreSQL native `ENUM`, `ARRAY` contains/overlap operators, `JSONB` path operators, Row Level Security - RLS):
      1. Bắt buộc khai báo rõ trong `docs/specs/<feature-slug>/plan.md`.
      2. Sử dụng `.with_variant(...)` nếu có thể để cung cấp kiểu tương thích fallback cho SQLite.
      3. Yêu cầu `qa-tester` gắn decorator `@pytest.mark.postgres_only` vào các test case kiểm tra tính năng này để SQLite test suite tự động skip an toàn khi chạy offline sandbox.
      4. Hỗ trợ chạy test trực tiếp trên PostgreSQL engine qua `TEST_DATABASE_URL=postgresql+asyncpg://...`.
- **Chống lỗi N+1**: Toàn bộ quan hệ nạp trong `AsyncSession` phải sử dụng `selectinload()` hoặc `joinedload()`.

---

## 3. Tổ Chức Models, Migrations & Seeds
- **Auto-Discovery Models**: File `src/db/models/__init__.py` tự động nạp mọi model con cho Alembic autogenerate.
- **Phân tách Migration & Testing (Supabase / Local / Offline)**:
  - SQLite in-memory test (`:memory:`) được sinh bảng tự động qua `Base.metadata.create_all` trong `conftest.py`. Không áp dụng Alembic cho SQLite in-memory test.
  - Khi dùng Supabase: BẮT BUỘC dùng `DIRECT_DATABASE_URL` (Session Pooler hoặc Direct port `5432`, `ssl=require`) để chạy `alembic upgrade head`. Không dùng Transaction Pooler port `6543` vì không hỗ trợ prepared statements & session locks cho migration DDL.
  - Khi có PostgreSQL runtime local: Dùng `alembic upgrade head` (`docker compose up -d postgres`).
  - Trong sandbox / môi trường không có PostgreSQL: Chạy `PYTHONPATH=src .venv/bin/python src/db/migrations/generate_offline_migration.py <slug>` để tự động sinh file migration chuẩn xác (kèm ID revision hợp lệ) trong `src/db/migrations/versions/`, sau đó hoàn thiện logic `upgrade()` và `downgrade()`.
- **Seed Data**: Đặt tại `src/db/seeds/<module>_seed.py`, đảm bảo tính idempotent (kiểm tra tồn tại trước khi add). Chạy qua `PYTHONPATH=src .venv/bin/python src/db/seeds/runner.py`.
- **Bàn giao Wave Handshake (`[HANDSHAKE-HANDOVER]`)**: Khi hoàn thành models, migrations và seeds, `db-dev` gửi thông điệp chuẩn hóa kèm cờ `Contract Modified: TRUE/FALSE` và chi tiết thay đổi để Tech Lead thẩm định tại Handshake Gate trước khi kích hoạt Wave 2.

---

## 4. Tham Gia Vòng Lặp Sửa Lỗi (Feedback Loop Protocol)
Khi nhận tin nhắn điều phối `[SELF-HEALING ACTION REQUIRED]` từ QA hoặc `[REVIEW-FIX ACTION REQUIRED]` từ Reviewer:
1. Phân tích nguyên nhân và **chỉ chỉnh sửa trong phạm vi `src/db/`**.
2. Kiểm tra smoke check: `.venv/bin/ruff check src/db/` và `python3 -m py_compile src/db/...`.
3. Gửi thông điệp phản hồi `[FIX-COMPLETED]` cho Tech Lead Orchestrator:
   ```text
   [FIX-COMPLETED]
   - Feature: <feature-slug>
   - Iteration: <iteration_number>
   - Target Agent: db-dev
   - Modified Files: src/db/...
   - Contract Modified: TRUE | FALSE
   - Contract Changes: <chi tiết thay đổi schema/column nếu TRUE, hoặc NONE>
   - Resolved Bug/Finding IDs: <BUG-01 hoặc REV-01>
   - Summary of Fix: <tóm tắt ngắn giải pháp đã thực hiện>
   ```
