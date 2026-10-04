# Cẩm Nang Quy Trình Làm Việc Multi-Agent Dev Team (SOP)
### Chu trình Lập trình Dự án Chuẩn từ Ý tưởng đến Bàn giao trên Antigravity 2.0

Tài liệu này là **Quy trình Vận hành Chuẩn (Standard Operating Procedure - SOP)** dành cho **Product Owner / Tech Founder / Developer** điều phối hệ thống **Multi-Agent Dev Team** theo mô hình **Ma trận (Matrix Architecture)** kết hợp quy trình **2-Wave Execution** trên nền tảng **Antigravity 2.0**, giải quyết triệt để 4 trụ cột kỹ thuật: **Feedback Loop & Circuit Breaker**, **Data & API Contract Synchronization**, **CLI Execution Guardrails** và **Artifact Handover Schema**.

---

## 1. Sơ Đồ Quy Trình Vận Hành Toàn Diện (End-to-End Pipeline)

Mọi tính năng mới hoặc phân hệ nghiệp vụ đều vận hành qua chu trình 7 giai đoạn khép kín:

```text
[User / Product Owner]
          │ (Ý tưởng & Nhu cầu nghiệp vụ)
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 0: Tiếp nhận Ý tưởng & Định hình Phạm vi (Ideation & Scope)   │
│ - Xác định Feature Slug (kebab-case)                                    │
│ - Xác định Scope: Nghiệp vụ MVP (P0) vs Tính năng mở rộng (P1/P2)       │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 1: Thiết lập Hợp đồng Kỹ thuật & Kiến trúc (`planner`)        │
│ - Xuất bản: docs/specs/<feature-slug>/plan.md                           │
│   ├── Metadata Header (YAML Frontmatter chuẩn hóa)                      │
│   ├── Cross-Layer Data Contract Matrix (DB <-> Backend <-> Frontend)    │
│   ├── REST API Contract (Casing chuẩn snake_case + Error Schemas)       │
│   ├── UI Architecture (Next.js App Router 4 UI states tại src/frontend/)│
│   └── Acceptance Criteria & Test Matrix (AC-ID -> TC-ID)                │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ [Quality Gate 1: Duyệt plan.md]
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 2: Thiết lập Rào Chắn Dòng Lệnh & Thư viện (Guardrails)       │
│ - Áp dụng Role-based Command Whitelist & Blacklist nghiêm ngặt          │
│ - Rà soát dependencies: pyproject.toml & src/frontend/package.json      │
│ - Quy chuẩn Sandbox: Cắm cờ [DEPENDENCY REQUIRED], không chạy lệnh trần │
│ - Smoke check Day-0: .venv/bin/ruff check src/ sạch sẽ                  │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 3: Triển khai Lập trình Đợt kép (2-Wave Execution)            │
│                                                                         │
│ ┌──────────────────────────────────┐  ┌──────────────────────────────┐  │
│ │ Nhánh 1A: Database (`db-dev`)    │  │ Nhánh 1B: Frontend           │  │
│ │ - src/db/models/<name>.py        │  │           (`frontend-dev`)   │  │
│ │ - UUIDPrimaryKeyMixin, JSON array│  │ - TypeScript Types           │  │
│ │ - Alembic & Async Seeds          │  │ - Mock data fixtures         │  │
│ │ - Tránh N+1 (selectinload)       │  │ - UI 4 states (Loading,      │  │
│ └────────────────┬─────────────────┘  │   Error, Empty, Success)     │  │
│                  │ (Models sẵn sàng)  └──────────────────────────────┘  │
│                  ▼                                                      │
│ ┌──────────────────────────────────┐                                    │
│ │ Nhánh 2: Backend API             │                                    │
│ │          (`backend-dev`)         │                                    │
│ │ - src/backend/app/schemas/       │                                    │
│ │ - src/backend/app/services/      │                                    │
│ │ - src/backend/app/api/v1/        │                                    │
│ │   (Kết nối src/db/ qua PYTHONPATH)                                    │
│ └──────────────────────────────────┘                                    │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 4: Kiểm thử Tự động & Vòng lặp Sửa lỗi (`qa-tester`)          │
│ - 1. Linter: .venv/bin/ruff check src/                                  │
│ - 2. DB & Backend Tests: PYTHONPATH=src .venv/bin/pytest -v             │
│   (SQLite async in-memory fallback cô lập + Contract Verification Test) │
│ - 3. Frontend Typecheck: npm --prefix src/frontend run typecheck        │
│ - Xuất bản: docs/specs/<feature-slug>/test-report.md                    │
│                                                                         │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ [Vòng lặp Self-Healing] Nếu FAILED:                                │  │
│ │ Tech Lead gửi tin nhắn: [SELF-HEALING ACTION REQUIRED]             │  │
│ │ Dev Squad sửa lỗi -> Gửi phản hồi: [FIX-COMPLETED]                 │  │
│ │ QA kiểm thử lại (Tối đa 3 vòng lặp -> Kích hoạt Circuit Breaker)   │  │
│ └────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ [Quality Gate 2: Test PASSED 100%]
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 5: Thẩm định Code, Tối ưu & Bảo mật (`code-reviewer`)         │
│ - Token-Optimized Audit qua `git status --short` và `git diff`          │
│ - Quality Gate Scorecard: Contract Sync, OWASP, N+1 Query, A11y         │
│ - Xuất bản: docs/specs/<feature-slug>/review-report.md                  │
│                                                                         │
│ ┌────────────────────────────────────────────────────────────────────┐  │
│ │ [Vòng lặp Review Feedback] Nếu CHANGES_REQUESTED:                  │  │
│ │ Tech Lead gửi tin nhắn: [REVIEW-FIX ACTION REQUIRED]               │  │
│ │ Dev Squad sửa lỗi -> Gửi phản hồi: [FIX-COMPLETED]                 │  │
│ │ QA chạy lại test -> Reviewer thẩm định lại (Tối đa 3 vòng lặp)     │  │
│ └────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ [Quality Gate 3: Verdict APPROVED]
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 6: Đóng gói, Git Commit & Bàn giao (Tech Lead Orchestrator)   │
│ - Kiểm tra git status --short & rà soát dependencies manifest           │
│ - Tạo Conventional Commit: feat(<feature-slug>): ...                    │
│ - Bàn giao báo cáo nghiệm thu & Hướng dẫn User trải nghiệm              │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Bảng Phân Công Trách Nhiệm, Model Tiering & Rào Chắn Lệnh (RACI Matrix)

| Vai trò / Tác tử | Nhận diện Subagent | Antigravity Model | Thư mục sở hữu (Ownership) | Lệnh được phép (Whitelist) | Lệnh cấm (Blacklist) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Product Owner** | User (Con người) | - | Toàn dự án | Mọi lệnh hệ thống | - |
| **Tech Lead** | Antigravity Main Agent | `inherit` | Toàn dự án | Điều phối subagents, `python3 -m py_compile src/db/models/*.py` (Wave Gate), `git status`, `git add`, `git commit` | Cấm `git reset --hard`, `git push --force` |
| **Architect** | [`planner`](.agents/agents/planner.md) | `pro` (Reasoning sâu) | `docs/specs/<slug>/` | Chỉ đọc/ghi file (`view_file`, `write_to_file`) | Cấm chạy shell commands làm đổi code |
| **DB Specialist** | [`db-dev`](.agents/agents/db-dev.md) | `inherit` | `src/db/` | `.venv/bin/ruff check src/db/`, `python3 -m py_compile`, `generate_offline_migration.py`, `alembic`, `runner.py` | Cấm `rm -rf`, `dropdb`, `pip install`, ghi file ngoài `src/db/` |
| **Frontend Dev** | [`frontend-dev`](.agents/agents/frontend-dev.md) | `inherit` / `flash` | `src/frontend/` | `npm --prefix src/frontend run typecheck`, `run lint`, `run build` | Cấm `npm install` trần, ghi file ngoài `src/frontend/` |
| **Backend Dev** | [`backend-dev`](.agents/agents/backend-dev.md) | `inherit` | `src/backend/` | `.venv/bin/ruff check src/backend/`, `python3 -m py_compile` | Cấm `pip install` trần, ghi file ngoài `src/backend/` |
| **QA Specialist** | [`qa-tester`](.agents/agents/qa-tester.md) | `flash` (Tiết kiệm 60% latency & token) | `docs/specs/`, `tests/` | `.venv/bin/ruff check src/`, `PYTHONPATH=src .venv/bin/pytest`, `run typecheck` | Cấm tự ý sửa code nghiệp vụ trong `src/` |
| **Code Reviewer** | [`code-reviewer`](.agents/agents/code-reviewer.md) | `pro` (Audit bảo mật OWASP) | `docs/specs/` | `git status --short`, `git diff --stat`, `git diff -- src/ docs/ ':!*package-lock.json' ':!*.lock'`, `git diff` | Cấm chạy lệnh sửa code hoặc thay đổi git |

---

## 3. Chi Tiết 7 Giai Đoạn Vận Hành

---

### Giai đoạn 0: Tiếp nhận Ý tưởng & Định hình Phạm vi (Ideation & Scope)
- **Đặt Feature Slug**: Định danh ngắn gọn dạng `kebab-case` (ví dụ: `auth-system`, `inventory-tracking`, `order-management`). Slug này sẽ là tên thư mục chứa hồ sơ: `docs/specs/<feature-slug>/`.
- **Phân ranh giới MVP**: Ghi rõ các tính năng P0 (bắt buộc có ngay) và P1/P2 (mở rộng sau này).

---

### Giai đoạn 1: Thiết lập Hợp đồng Kỹ thuật & Kiến trúc (`planner`)
- Tech Lead kích hoạt `planner` (tham chiếu [plan-template.md](.agents/skills/team-pipeline/resources/plan-template.md)).
- `planner` khảo sát hiện trạng `src/` và xuất bản `docs/specs/<feature-slug>/plan.md` chứa:
  1. **Header Metadata**: YAML frontmatter (`feature_slug`, `version`, `status`, `iteration`).
  2. **Cross-Layer Data Contract Matrix**: Bảng ánh xạ 3 tầng đồng bộ 100% tên trường (`snake_case`), kiểu dữ liệu giữa SQLAlchemy, Pydantic v2 và TypeScript Strict.
  3. **REST API Contract**: Endpoints, HTTP methods, Request/Response JSON và chuẩn hóa thông báo lỗi `{"detail": "..."}`.
  4. **Wave 1 Mock Fixtures**: Dữ liệu mẫu tại `src/frontend/src/lib/api/mocks/<resource>.ts`.
  5. **UI Architecture**: Next.js App Router và xử lý đủ **4 trạng thái UI** (`Loading`, `Error`, `Empty`, `Success`).
  6. **Ma trận Truy xuất Yêu cầu**: Liên kết trực tiếp giữa Tiêu chí Nghiệm thu (`AC-ID`) và Kịch bản Test (`TC-ID`).

> 🛡️ **Quality Gate 1**: Duyệt `plan.md`. Không viết code khi chưa có hợp đồng chuẩn này.

---

### Giai đoạn 2: Thiết lập Rào Chắn Dòng Lệnh & Thư viện (Guardrails)
- Rà soát các thư viện phát sinh trong `pyproject.toml` và `src/frontend/package.json`.
- Áp dụng quy chuẩn Sandbox: Không chạy `pip/npm install` trần khi không có mạng; cập nhật manifest và cắm cờ `[DEPENDENCY REQUIRED]`.
- Chạy smoke check Day-0: `.venv/bin/ruff check src/` để chắc chắn không có lỗi cú pháp tồn dư.

---

### Giai đoạn 3: Triển khai Lập trình Đợt kép (2-Wave Execution)
- **Chiến lược Không gian làm việc (`Workspace: "inherit"`)**:
  - Khi Tech Lead gọi `invoke_subagent` cho các Dev Squads, bắt buộc cấu hình `"Workspace": "inherit"`. Vì `db-dev` (`src/db/`), `frontend-dev` (`src/frontend/`) và `backend-dev` (`src/backend/`) có phạm vi thư mục hoàn toàn tách biệt, việc dùng chung workspace không gây xung đột Git, đồng thời giúp Wave 2 và QA nhìn thấy code mới ngay lập tức mà không cần merge branch.
- **Quản lý Định danh Hội thoại (Squad Conversation Registry)**:
  - Tech Lead Orchestrator **BẮT BUỘC lưu lại Conversation ID** của từng squad:
    `SQUAD_REGISTRY = {"db-dev": conv_id_db, "frontend-dev": conv_id_fe, "backend-dev": conv_id_be}`
  - Registry này được duy trì để định tuyến thông điệp sửa lỗi qua `send_message`, bảo toàn 100% ngữ cảnh hội thoại.
- **Quy tắc phân vùng file tuyệt đối (File Ownership Isolation)**:
  - `db-dev`: Chỉ ghi trong `src/db/`.
  - `frontend-dev`: Chỉ ghi trong `src/frontend/`.
  - `backend-dev`: Chỉ ghi trong `src/backend/`.

#### Đợt 1 (Wave 1 - Triển khai song song):
- **Nhánh 1A - Database Specialist (`db-dev` tại `src/db/` — `Model: "inherit"`)**:
  - Tạo model trong `src/db/models/<name>.py` (kế thừa `UUIDPrimaryKeyMixin` và `TimestampMixin`).
  - Mảng dữ liệu dùng `JSON` (kèm variant PG nếu cần) để SQLite test không bị lỗi.
  - Khi dùng tính năng độc quyền PostgreSQL (`pgvector`, `tsvector`, native enum, JSONB path), khai báo rõ trong `plan.md` và dùng `.with_variant(...)` cho SQLite fallback.
  - Viết repository async chống N+1 bằng `selectinload()`.
  - **Quản lý Migration & Supabase**:
    - Khi dùng Supabase: BẮT BUỘC dùng `DIRECT_DATABASE_URL` (Session Mode port 5432, `ssl=require`) để chạy `alembic upgrade head`. Không dùng Transaction Pooler port 6543 vì không hỗ trợ prepared statements & session locks cho migration DDL.
    - Khi có PostgreSQL runtime local: `alembic revision --autogenerate -m "<slug>"`.
    - Khi trong Sandbox / không có DB live: `PYTHONPATH=src .venv/bin/python src/db/migrations/generate_offline_migration.py <slug>` để tự động tạo migration skeleton chuẩn có ID hợp lệ, sau đó điền `op.create_table()` và `op.drop_table()`.
  - Tạo kịch bản seed dữ liệu mẫu idempotent tại `src/db/seeds/<name>_seed.py`.
- **Nhánh 1B - Frontend Specialist (`frontend-dev` tại `src/frontend/` — `Model: "inherit"`)**:
  - Tạo TypeScript types tại `src/frontend/src/types/` khớp 100% với Data Contract Matrix (`snake_case`, 0 `any`).
  - Tạo mock fixtures tại `src/frontend/src/lib/api/mocks/` hỗ trợ `isMockMode()` và cờ `NEXT_PUBLIC_USE_MOCKS=true`.
  - Xây dựng UI components & pages Next.js Server Component-First xử lý trọn vẹn 4 trạng thái: Loading (loading.tsx), Error (error.tsx), Empty, Success.
  - Tự động hóa phân giải API URL: `getApiBaseUrl()` (hỗ trợ SSR `INTERNAL_API_URL` và Client `NEXT_PUBLIC_API_URL`).
  - Kiểm tra kiểu: `npm --prefix src/frontend run typecheck`.

#### Wave Handshake Gate (Chốt kiểm tra chéo giữa Wave 1 & Wave 2):
Trước khi kích hoạt `backend-dev` (Wave 2), Tech Lead Orchestrator thực hiện kiểm tra nhanh:
```bash
python3 -m py_compile src/db/models/*.py
.venv/bin/ruff check src/db/
```
- Xác nhận `src/db/models/__init__.py` đã export các models mới.
- *Nếu phát hiện lỗi cú pháp hoặc import*: DỪNG LẠI, KHÔNG khởi chạy `backend-dev` mà gửi ngay `[SELF-HEALING ACTION REQUIRED]` qua `send_message` tới `SQUAD_REGISTRY["db-dev"]`. Chỉ khi models sạch sẽ mới chuyển giao cho Wave 2.

#### Đợt 2 (Wave 2 - Kết nối Backend & Đồng bộ Live API):
- **Backend Specialist (`backend-dev` tại `src/backend/` — `Model: "inherit"`)**:
  - Kích hoạt ngay sau khi vượt qua Wave Handshake Gate, Tech Lead lưu lại `conv_id_be`.
  - Viết Pydantic v2 schemas tại `src/backend/app/schemas/` (`ConfigDict(from_attributes=True)`, giới hạn `max_length`, `ge`/`le`).
  - Viết Services xử lý business logic và transaction tại `src/backend/app/services/`.
  - Viết API routers tại `src/backend/app/api/v1/endpoints/` kết nối models trực tiếp từ `src/db/` thông qua `PYTHONPATH=src`. Expose cả `/health` và `/api/v1/health`.
  - Cắm router vào `api_router` tập trung tại `src/backend/app/api/v1/router.py`.
  - **Đồng bộ Mock → Live API & Cache Invalidation**:
    - Chuyển `NEXT_PUBLIC_USE_MOCKS=false` trong `.env`.
    - Typed API Client trong `src/frontend/src/lib/api/client.ts` tự động áp dụng `cache: 'no-store'`, header `Cache-Control: 'no-cache'`, và gọi `clearClientApiCache()` để xóa sạch stale cache cả ở Storage và Browser CacheStorage.
    - Chạy script kiểm tra mạng nhanh: `.venv/bin/python scripts/verify_network.py`.

---

### Giai đoạn 4: Kiểm thử Tự động & Vòng lặp Sửa lỗi (`qa-tester`)
- `qa-tester` đối chiếu `plan.md` và viết test tự động tại `src/backend/tests/test_<feature>.py`.
- **Quy Chuẩn Kiểm Thử Kiểu Dữ Liệu PostgreSQL Nâng Cao (Cross-DB Testing)**:
  - Khi test các tính năng đặc thù PostgreSQL (`pgvector`, `tsvector`, native enum, array operators), gắn decorator `@pytest.mark.postgres_only`.
  - SQLite in-memory test mặc định sẽ tự động skip an toàn các test này mà không báo `FAILED`.
  - Khi có PostgreSQL: `TEST_DATABASE_URL=postgresql+asyncpg://... PYTHONPATH=src .venv/bin/pytest src/backend/tests -v`.
- Thực thi chuỗi lệnh kiểm tra:
  ```bash
  # 1. Linter & Code Standards
  .venv/bin/ruff check src/

  # 2. Backend & DB Testing (SQLite in-memory fallback + Contract Verification)
  PYTHONPATH=src ./.venv/bin/pytest src/backend/tests -v

  # 3. Frontend TypeScript Integrity
  npm --prefix src/frontend run typecheck
  ```
- Xuất báo cáo tại `docs/specs/<feature-slug>/test-report.md` (kèm Chỉ số Metrics và Structured Bug Tickets).
- **Vòng lặp Self-Healing (Tự sửa lỗi) & Bảo Toàn Ngữ Cảnh (Context Preservation)**:
  - Nếu `overall_status: FAILED`:
    - **Bảo toàn Ngữ cảnh**: Tech Lead **BẮT BUỘC dùng `send_message`** gửi yêu cầu sửa lỗi tới Conversation ID của squad (`SQUAD_REGISTRY[target_agent]`). TUYỆT ĐỐI KHÔNG gọi `invoke_subagent` mới.
    - Dev Squad sửa lỗi trong thư mục phân quyền, chạy smoke test và gửi phản hồi `[FIX-COMPLETED]`.
    - `qa-tester` chạy lại bài test. Bộ đếm `iteration` tăng thêm 1.
    - **Cơ chế Ngắt Mạch (Circuit Breaker)**: Tối đa **3 vòng lặp**. Nếu quá 3 lần vẫn lỗi, kích hoạt Giao thức Báo cáo Leo thang cho User.

> 🛡️ **Quality Gate 2**: Toàn bộ test suite phải đạt trạng thái `PASSED 100%`.

---

### Giai đoạn 5: Thẩm định Code, Tối ưu & Bảo mật (`code-reviewer`)
- **Quy trình Thẩm định Tiết kiệm Token (Token-Optimized Audit Protocol)**:
  1. `git status --short`: Quét nhanh biến động file mới (`??`) và file sửa đổi (`M`).
  2. `git diff --stat`: Đo lường quy mô và phân bố dòng thay đổi.
  3. `git diff -- src/ docs/ ':!*package-lock.json' ':!*.lock'`: Lọc bỏ lockfiles hoặc minified files, dồn 100% token budget vào logic nghiệp vụ và kiến trúc.
- **Bảng Cổng Chất Lượng (Quality Gate Scorecard)**:
  1. *Khớp Hợp đồng*: Tên trường JSON và kiểu dữ liệu có khớp 100% với Data Contract Matrix trong `plan.md` không?
  2. *Database*: Có truy vấn N+1 không? Có thiếu index cho trường lọc không?
  3. *Bảo mật*: Pydantic v2 validation đã giới hạn độ dài chưa? Có lộ secrets ra response không?
  4. *Frontend*: Có ép kiểu `any` không? Xử lý đủ 4 trạng thái UI và A11y chưa?
  5. *Độ phủ Kiểm thử*: 100% test cases đã pass chưa?
- **Xuất bản báo cáo**: `docs/specs/<feature-slug>/review-report.md`.
  - Nếu `CHANGES_REQUESTED`: Tech Lead gửi `[REVIEW-FIX ACTION REQUIRED]`. Dev Squad sửa và gửi `[FIX-COMPLETED]`. QA re-test để chống lỗi hồi quy, Reviewer re-review (tối đa 3 vòng lặp).
  - Nếu `APPROVED`: Chuyển sang Giai đoạn 6.

> 🛡️ **Quality Gate 3**: Verdict bắt buộc phải đạt `APPROVED`.

---

### Giai đoạn 6: Đóng gói, Git Commit & Bàn giao (Tech Lead Orchestrator)
1. Rà soát `git status --short` kiểm tra toàn bộ file mới và sửa đổi trong `src/`, `docs/specs/<feature-slug>/`, `pyproject.toml`, `package.json`.
2. Thực thi commit chuẩn hóa (Conventional Commits):
   ```bash
   git add src/ docs/specs/<feature-slug>/
   git add pyproject.toml src/frontend/package*.json 2>/dev/null || true
   git commit -m "feat(<feature-slug>): implement <tên tính năng ngắn gọn>

   - DB: add SQLAlchemy 2.0 models & migrations in src/db/
   - Backend: implement FastAPI schemas, services & endpoints in src/backend/
   - Frontend: build Next.js UI components & typed API client in src/frontend/
   - Quality: 100% automated tests passed, code review approved
   - Specs: docs/specs/<feature-slug>/plan.md"
   ```
3. Bàn giao cho User: Cung cấp Commit Hash, danh sách files, tài liệu trong `docs/specs/<feature-slug>/` và hướng dẫn kiểm chứng tính năng.

---

## 4. Bộ Mẫu Thông Điệp Điều Phối Nội Bộ (Standard Dispatch Protocol)

### Mẫu 1: Gửi từ Tech Lead khi QA FAILED (`[SELF-HEALING ACTION REQUIRED]`)
```text
[SELF-HEALING ACTION REQUIRED]
- Feature: <feature-slug>
- Iteration: <iteration_number> / 3
- Target Agent: db-dev (src/db/) | backend-dev (src/backend/) | frontend-dev (src/frontend/)
- Target File & Line: <đường_dẫn_file>#L...
- Failed Test ID: <mã test case hoặc tên hàm test>
- Diagnostics & Traceback:
  <dán nội dung traceback hoặc lỗi chi tiết từ Mục 4 test-report.md>
- Reproduction Command: <lệnh chạy lại để tái hiện lỗi>
- Instructions: Phân tích nguyên nhân và khắc phục triệt để. TUYỆT ĐỐI chỉ chỉnh sửa trong thư mục được phân quyền của bạn. Sau khi hoàn tất và smoke test sạch sẽ, gửi báo cáo [FIX-COMPLETED] để tiến hành kiểm thử lại.
```

### Mẫu 2: Gửi từ Tech Lead khi Review CHANGES_REQUESTED (`[REVIEW-FIX ACTION REQUIRED]`)
```text
[REVIEW-FIX ACTION REQUIRED]
- Feature: <feature-slug>
- Iteration: <iteration_number> / 3
- Target Agent: db-dev (src/db/) | backend-dev (src/backend/) | frontend-dev (src/frontend/)
- Finding ID: <REV-01, ...>
- Severity: [CRITICAL] | [MAJOR]
- Target File & Line: <đường_dẫn_file>#L...
- Issue Description & Diff:
  <trích xuất mô tả vi phạm và code diff từ Mục 3 review-report.md>
- Remediation Guidance: <hướng dẫn sửa đổi của reviewer>
- Instructions: Khắc phục đúng các điểm vi phạm trên trong thư mục phân quyền. Chạy smoke test và gửi báo cáo [FIX-COMPLETED] khi hoàn tất.
```

### Mẫu 3: Gửi từ Dev Squad khi Hoàn Tất Sửa Lỗi (`[FIX-COMPLETED]`)
```text
[FIX-COMPLETED]
- Feature: <feature-slug>
- Iteration: <iteration_number>
- Target Agent: <db-dev | backend-dev | frontend-dev>
- Modified Files: <danh sách files đã sửa>
- Contract Modified: TRUE | FALSE
- Contract Changes: <chi tiết thay đổi schema/endpoint nếu TRUE, hoặc NONE>
- Resolved Bug/Finding IDs: <BUG-01, REV-01, ...>
- Summary of Fix: <tóm tắt ngắn gọn giải pháp khắc phục và kết quả smoke test cục bộ>
```
*Lưu ý cho Tech Lead*: Nếu `Contract Modified: TRUE`, Tech Lead bắt buộc cập nhật lại `docs/specs/<feature-slug>/plan.md`, nâng `version` (e.g. `1.1.0`), đồng bộ lại Cross-Layer Data Contract Matrix và thông báo cho squad liên quan trước khi chạy lại QA.

### Mẫu 4: Báo Cáo Leo Thang Khi Kích Hoạt Circuit Breaker (`[CIRCUIT BREAKER ESCALATION]`)
```text
[CIRCUIT BREAKER ESCALATION]
- Feature: <feature-slug>
- Status: PAUSED_FOR_HUMAN_INTERVENTION
- Iterations Executed: 3 / 3
- Root Cause Summary: <tóm tắt lý do hệ thống không tự khắc phục được sau 3 lần lặp>
- Blocking Issues: <danh sách các bài test hoặc findings còn tắc nghẽn>
- Proposed Solutions: <đề xuất giải pháp cho PO / User xem xét can thiệp>
```

---

## 5. Bảng Tiêu Chí Kiểm Tra Nhanh Chất Lượng (Quality Checklist)

Dùng bảng này để nghiệm thu sản phẩm sau mỗi tính năng:

- [ ] `docs/specs/<feature-slug>/plan.md` có đầy đủ Metadata, Data Contract Matrix, API Spec và UI Spec.
- [ ] Toàn bộ API payload và Pydantic schemas sử dụng thống nhất chuẩn `snake_case`.
- [ ] Model trong `src/db/models/` kế thừa `UUIDPrimaryKeyMixin` và `TimestampMixin`.
- [ ] Không có truy vấn N+1 (`selectinload` được dùng đầy đủ cho relationships).
- [ ] Endpoint FastAPI có Pydantic v2 validation giới hạn độ dài chuỗi và khoảng giá trị số.
- [ ] Giao diện Next.js hiển thị đầy đủ 4 trạng thái: Loading skeleton, Error message, Empty state, Success state.
- [ ] Không có từ khóa `any` trong toàn bộ code TypeScript (`src/frontend/`).
- [ ] `.venv/bin/ruff check src/` trả về `All checks passed!`.
- [ ] `PYTHONPATH=src .venv/bin/pytest src/backend/tests` đạt `100% passed`.
- [ ] `npm --prefix src/frontend run typecheck` không có lỗi type.
- [ ] `docs/specs/<feature-slug>/review-report.md` đạt Verdict `APPROVED`.
- [ ] Git commit được tạo theo đúng chuẩn Conventional Commits.

---

## 6. Hướng Dẫn Xử Lý Sự Cố Thường Gặp (Troubleshooting)

### Vấn đề 1: Pytest báo lỗi `aiosqlite is not installed` hoặc không tìm thấy module `backend`
* **Nguyên nhân**: Chạy lệnh pytest trần mà không chỉ định virtualenv hoặc thiếu `PYTHONPATH`.
* **Cách khắc phục**: Luôn chạy bằng lệnh chuẩn hóa:
  ```bash
  PYTHONPATH=src .venv/bin/pytest src/backend/tests -v
  ```

### Vấn đề 2: Lỗi SQLite `CompileError: Compiler <...> can't render element of type ARRAY`
* **Nguyên nhân**: Model dùng kiểu `ARRAY` trần của PostgreSQL, khiến SQLite in-memory test không thể render bảng.
* **Cách khắc phục**: Chuyển sang dùng `from sqlalchemy import JSON` với `default=list` hoặc dùng variant `JSON().with_variant(ARRAY(String), "postgresql")`.

### Vấn đề 3: Lỗi `MissingGreenlet` khi truy cập relationship trong FastAPI
* **Nguyên nhân**: Trong môi trường bất đồng bộ (`AsyncSession`), truy cập lazy-loading relationship mà không dùng `await`.
* **Cách khắc phục**: Tại tầng repository, luôn thêm `.options(selectinload(Model.relation_name))` vào câu lệnh `select()`.

### Vấn đề 4: Sandbox không có internet khi subagent chạy `npm/pip install`
* **Nguyên nhân**: Môi trường sandbox được cô lập để bảo mật.
* **Cách khắc phục**: Tuyệt đối không cho agent chạy lệnh cài đặt trần. Cập nhật tên thư viện vào `pyproject.toml` hoặc `src/frontend/package.json` và gắn cờ `[DEPENDENCY REQUIRED]`.

### Vấn đề 5: Supabase văng lỗi `prepared statement "__asyncpg_stmt_..." does not exist` khi chạy Alembic
* **Nguyên nhân**: Kết nối Alembic DDL migrations qua Supavisor Transaction Pooler (port `6543`). Transaction mode ngắt kết nối session sau mỗi lệnh và không hỗ trợ prepared statement của asyncpg.
* **Cách khắc phục**: Cấu hình `DIRECT_DATABASE_URL` trỏ trực tiếp vào Session Mode (port `5432`):
  `postgresql+asyncpg://postgres.[REF]:[PASS]@aws-0-[REGION].pooler.supabase.com:5432/postgres?ssl=require`.
  Đối với FastAPI App runtime (port `6543`), engine đã tự động đặt `prepared_statement_cache_size = 0`.

### Vấn đề 6: Next.js 15 Client hiển thị dữ liệu Mock cũ sau khi đã chuyển sang Live API
* **Nguyên nhân**: Router cache hoặc fetch cache của trình duyệt vẫn giữ response mock trước đó.
* **Cách khắc phục**: `src/frontend/src/lib/api/client.ts` đã được thiết lập `cache: 'no-store'` khi `isMockMode() === false`. Ngoài ra, gọi hàm `clearClientApiCache()` để dọn sạch sessionStorage/localStorage.
