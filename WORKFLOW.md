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
┌───────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 0: Phỏng vấn, Làm rõ Yêu cầu & Thiết lập PRD (`ba`)             │
│ - Tiếp nhận prompt từ User, phát hiện điểm mù & kịch bản góc (Edge Cases) │
│ - Phỏng vấn tương tác qua công cụ `ask_question`                          │
│ - Xuất bản: docs/specs/<feature-slug>/prd.md (FRs, BRs, ECs, BACs)        │
└───────────────────────────────────┬───────────────────────────────────────┘
                                    │ [Quality Gate 0: User duyệt prd.md]
                                    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 1: Thiết lập Hợp đồng Kỹ thuật & Kiến trúc (`planner`)          │
│ - Đầu vào: docs/specs/<feature-slug>/prd.md                               │
│ - Xuất bản: docs/specs/<feature-slug>/plan.md                             │
│   ├── Metadata Header (YAML Frontmatter chuẩn hóa)                        │
│   ├── Cross-Layer Data Contract Matrix (DB <-> Backend <-> Frontend/Mobile)│
│   ├── REST API Contract (Casing chuẩn snake_case + Error Schemas)         │
│   ├── UI Architecture (Next.js / Vite / React Native Expo 4 UI states)    │
│   └── Acceptance Criteria Matrix (BAC/FR -> AC-ID -> TC-ID)               │
└───────────────────────────────────┬───────────────────────────────────────┘
                                    │ [Quality Gate 1: Duyệt plan.md]
                                    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 2: Thiết lập Rào Chắn Dòng Lệnh & Thư viện (Guardrails)         │
│ - Áp dụng Role-based Command Whitelist & Blacklist nghiêm ngặt            │
│ - Rà soát dependencies: pyproject.toml, package.json (Web & Mobile)       │
│ - Quy chuẩn Sandbox: Cắm cờ [DEPENDENCY REQUIRED], không chạy lệnh trần   │
│ - Smoke check Day-0: .venv/bin/ruff check src/ sạch sẽ                    │
└───────────────────────────────────┬───────────────────────────────────────┘
                                    │
                                    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 3: Triển khai Lập trình Đợt kép (2-Wave Pipelined Execution)    │
│                                                                           │
│  ┌──────────────────────────────────┐   ┌──────────────────────────────┐  │
│  │ Nhánh 1A: Database (`db-dev`)    │   │ Nhánh 1B: Frontend & Mobile  │  │
│  │ - src/db/models/<name>.py        │   │           (`frontend-dev`)   │  │
│  │ - UUIDPrimaryKeyMixin, JSON array│   │ - Web: Next.js / React Vite  │  │
│  │ - Alembic & Async Seeds          │   │ - Mobile: React Native Expo  │  │
│  │ - Tránh N+1 (selectinload)       │   │ - TypeScript Types & Mocks   │  │
│  └────────────────┬─────────────────┘   │ - UI 4 states (Load/Err/...) │  │
│                   │ [Handshake Gate]    │   (Chạy song song gối đầu)   │  │
│                   ▼                     │                              │  │
│  ┌──────────────────────────────────┐   │                              │  │
│  │ Nhánh 2: Backend API             │◄──┘                              │  │
│  │          (`backend-dev`)         │ (Đồng bộ Mock -> Live API)       │  │
│  │ - src/backend/app/schemas/       │                                  │  │
│  │ - src/backend/app/services/      │                                  │  │
│  │ - src/backend/app/api/v1/        │                                  │  │
│  │   (Kích hoạt ngay khi DB xong)   │                                  │  │
│  └──────────────────────────────────┘                                  │  │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     │
                                     ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 4: Kiểm thử Tự động & Vòng lặp Sửa lỗi (`qa-tester`)            │
│ - 1. Linter: python -m ruff check src/                                    │
│ - 2. Contract Sync: python scripts/verify_contracts.py <feature-slug>     │
│ - 3. Migration DAG: python scripts/verify_migrations.py                   │
│ - 4. DB & Backend Tests: python -m pytest src/backend/tests src/db/tests  │
│   (SQLite async in-memory fallback cô lập + Migration DAG integrity)      │
│ - 5. Client Typecheck: npm run typecheck (cả Web src/frontend/ & Mobile)  │
│ - Xuất bản: docs/specs/<feature-slug>/test-report.md                      │
│                                                                           │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ [Vòng lặp Self-Healing] Nếu FAILED:                                │   │
│  │ Tech Lead gửi tin nhắn: [SELF-HEALING ACTION REQUIRED]             │   │
│  │ (Cắt tỉa 15-25 dòng traceback trọng tâm chống phình ngữ cảnh)      │   │
│  │ Dev Squad sửa lỗi -> Gửi phản hồi: [FIX-COMPLETED]                 │   │
│  │ QA kiểm thử lại (Tối đa 3 vòng lặp -> Kích hoạt Circuit Breaker)   │   │
│  └────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────┬──────────────────────────────────────┘
                                     │ [Quality Gate 2: Test PASSED 100%]
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 5: Thẩm định Code, Tối ưu & Bảo mật (`code-reviewer`)          │
│ - Token-Optimized Audit qua `git status --short` và `git diff`           │
│ - Quality Gate Scorecard: Contract Sync, OWASP, N+1 Query, A11y          │
│ - Xuất bản: docs/specs/<feature-slug>/review-report.md                   │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ [Vòng lặp Review Feedback] Nếu CHANGES_REQUESTED:                  │  │
│  │ Tech Lead gửi tin nhắn: [REVIEW-FIX ACTION REQUIRED]               │  │
│  │ Dev Squad sửa lỗi -> Gửi phản hồi: [FIX-COMPLETED]                 │  │
│  │ QA chạy lại test -> Reviewer thẩm định lại (Tối đa 3 vòng lặp)     │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬──────────────────────────────────────┘
                                    │ [Quality Gate 3: Verdict APPROVED]
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 6: Đóng gói, Git Commit & Dọn dẹp (Tech Lead Orchestrator)     │
│ - Kiểm tra git status --short & cập nhật manifest dependencies độc quyền │
│ - Tạo Conventional Commit: feat(<feature-slug>): ...                     │
│ - Tự động dọn dẹp subagents qua manage_subagents(Action="kill")          │
│ - Bàn giao báo cáo nghiệm thu & Hướng dẫn User trải nghiệm               │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Bảng Phân Công Trách Nhiệm, Model Tiering & Rào Chắn Lệnh (RACI Matrix)

| Vai trò / Tác tử | Nhận diện Subagent | Antigravity Model | Thư mục sở hữu (Ownership) | Lệnh được phép (Whitelist) | Lệnh cấm (Blacklist) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Product Owner** | User (Con người) | - | Toàn dự án | Mọi lệnh hệ thống | - |
| **Tech Lead** | Antigravity Main Agent | `inherit` | Toàn dự án | Điều phối subagents, `manage_subagents` (dọn dẹp), độc quyền cập nhật manifest (`pyproject.toml`, `package.json`), `python -m py_compile src/db/models/*.py` (Wave Gate), `python scripts/verify_contracts.py`, `python scripts/verify_migrations.py`, `python scripts/start_dev.py`, `python scripts/smoke_test.py`, `git status`, `git add`, `git commit` | Cấm `git reset --hard`, `git push --force` |
| **Business Analyst** | [`ba`](.agents/agents/ba.md) | `pro` (Phân tích nghiệp vụ sâu) | `docs/specs/<slug>/` | Phỏng vấn tối ưu 1-3 câu P0 (`ask_question`), chỉ đọc/ghi file (`view_file`, `write_to_file`, `replace_file_content`) | Cấm chạy shell commands, cấm sửa code hoặc file cấu hình gốc |
| **Architect** | [`planner`](.agents/agents/planner.md) | `pro` (Reasoning sâu) | `docs/specs/<slug>/` | Chỉ đọc/ghi file tài liệu (`view_file`, `write_to_file`) | Cấm chạy shell commands, cấm sửa code hoặc file cấu hình gốc |
| **DB Specialist** | [`db-dev`](.agents/agents/db-dev.md) | `inherit` | `src/db/` | `python -m ruff check src/db/`, `python -m py_compile src/db/...`, `generate_offline_migration.py`, `verify_migrations.py`, `runner.py`, `alembic` | Cấm `rm -rf`, `dropdb`, cấm sửa `pyproject.toml`, cấm `pip install`, ghi file ngoài `src/db/` |
| **Frontend & Mobile Dev** | [`frontend-dev`](.agents/agents/frontend-dev.md) | `inherit` / `flash` | `src/frontend/`, `src/mobile/` | Web: `npm --prefix src/frontend run typecheck`, `run lint`, `run build`; Mobile: `npm --prefix src/mobile run typecheck`, `run lint` | Cấm `npm install` trần, cấm tự ý sửa `package.json`, cấm remote fonts, ghi file ngoài `src/frontend/` và `src/mobile/` |
| **Backend Dev** | [`backend-dev`](.agents/agents/backend-dev.md) | `inherit` | `src/backend/` | `python -m ruff check src/backend/`, `python -m py_compile src/backend/...` | Cấm `pip install` trần, cấm sửa `pyproject.toml`, ghi file ngoài `src/backend/` |
| **QA Specialist** | [`qa-tester`](.agents/agents/qa-tester.md) | `flash` (Tiết kiệm 60% latency & token) | `docs/specs/`, `tests/` | 1-Click `python scripts/smoke_test.py`, `python -m ruff check src/`, `python scripts/verify_contracts.py`, `python scripts/verify_migrations.py`, `python -m pytest src/backend/tests src/db/tests`, `npm run typecheck` | Cấm tự ý sửa code nghiệp vụ trong `src/` hoặc file manifest |
| **Code Reviewer** | [`code-reviewer`](.agents/agents/code-reviewer.md) | `pro` (Audit bảo mật OWASP) | `docs/specs/` | `git status --short`, `git diff --stat`, `git diff -- src/ docs/ ':!*package-lock.json' ':!*.lock'`, `git diff` | Cấm chạy lệnh sửa code, git commit hoặc đổi file cấu hình |

---

## 3. Chi Tiết 7 Giai Đoạn Vận Hành

---

### Giai đoạn 0: Phỏng vấn, Làm rõ Yêu cầu, Bóc tách Epic & Thiết lập PRD (`ba`)
- **Vai trò thực hiện**: BA Agent ([`ba`](.agents/agents/ba.md), `Model: "pro"`).
- **Kỹ thuật thực hiện**:
  1. **Tiếp nhận prompt, Đặt Feature Slug & Đánh Giá Quy Mô (Granular Feature Slicing)**:
     - Định danh ngắn gọn dạng `kebab-case` (ví dụ: `auth-system`, `inventory-tracking`). Thư mục hồ sơ: `docs/specs/<feature-slug>/`.
     - **Định cỡ (T-Shirt Sizing)**:
       - *Atomic Feature (Size S/M)*: 1-3 user stories, tối đa 3-5 FRs, 1-2 DB models. Giữ nguyên làm 1 `<feature-slug>` duy nhất.
       - *Epic / Compound Feature (Size L/XL)*: Phân hệ rộng (> 5 FRs, nhiều domain aggregates như E-commerce, Quản lý kho, Thanh toán).
     - **Giao thức Bóc tách Epic (Epic Slicing Protocol)**:
       - TUYỆT ĐỐI KHÔNG dồn toàn bộ Epic vào 1 PRD duy nhất (gây phình token context và kéo dài vòng lặp phát triển).
       - BA Agent chủ động phân rã Epic thành chuỗi các Feature Slugs nguyên tử độc lập (ví dụ: `order-checkout` -> `order-payment` -> `order-fulfillment`), thiết lập bảng **Ma Trận Bóc Tách Epic (Mục 1.3 PRD)**, và ưu tiên lát cắt MVP (Phase 1 / P0) cho chu trình hiện tại.
  2. **Áp dụng High-Leverage Interview Protocol qua `ask_question`**:
     - **Giới hạn số lượng (Hard limit)**: Chỉ hỏi tối đa **1 đến 3 câu hỏi cốt lõi nhất (P0)** mang tính sống còn đối với kiến trúc hoặc phạm vi (MVP Scope / Lát cắt bóc tách ưu tiên, Personas & Quyền hạn, Quy tắc nghiệp vụ rẽ nhánh chính).
     - **Định dạng lựa chọn**: Luôn gom thành các phương án trắc nghiệm rõ ràng, đánh dấu tiền tố `(Recommended)` ở phương án khuyến nghị tối ưu nhất.
     - **Nguyên tắc Phân tách Nghiệp vụ vs Tiểu tiết**: TUYỆT ĐỐI KHÔNG làm phiền người dùng bằng các câu hỏi vụn vặt (UI styling, tên trường DB, các edge cases kỹ thuật thứ yếu). Thay vào đó, BA chủ động đề xuất giải pháp tối ưu trực tiếp vào bản thảo PRD.
  3. **Xuất bản PRD**: Biên soạn hoàn chỉnh `docs/specs/<feature-slug>/prd.md` theo mẫu chuẩn [prd-template.md](.agents/skills/team-pipeline/resources/prd-template.md).
- > 🛡️ **Quality Gate 0 (PRD Sign-off Gate)**: BA Agent tóm tắt các quyết định, lộ trình bóc tách Epic và đề xuất nghiệp vụ cho User để xin nghiệm thu một lần duy nhất. Khi User chấp thuận (`status: APPROVED_BY_USER`), Tech Lead mới kích hoạt `planner`.

---

### Giai đoạn 1: Thiết lập Hợp đồng Kỹ thuật & Kiến trúc (`planner`)
- Tech Lead kích hoạt `planner` với đầu vào là tài liệu PRD đã duyệt: `docs/specs/<feature-slug>/prd.md` (tham chiếu [plan-template.md](.agents/skills/team-pipeline/resources/plan-template.md)).
- `planner` khảo sát hiện trạng `src/` và xuất bản `docs/specs/<feature-slug>/plan.md` chứa:
  1. **Header Metadata**: YAML frontmatter (`feature_slug`, `version`, `status`, `iteration`, tham chiếu `prd.md`).
  2. **Cross-Layer Data Contract Matrix**: Bảng ánh xạ 3 tầng đồng bộ 100% tên trường (`snake_case`), kiểu dữ liệu giữa SQLAlchemy, Pydantic v2 và TypeScript Strict.
  3. **REST API Contract**: Endpoints, HTTP methods, Request/Response JSON và chuẩn hóa thông báo lỗi `{"detail": "..."}`.
  4. **Wave 1 Mock Fixtures**: Dữ liệu mẫu tại `src/frontend/src/lib/api/mocks/<resource>.ts`.
  5. **UI Architecture**: Next.js App Router và xử lý đủ **4 trạng thái UI** (`Loading`, `Error`, `Empty`, `Success`).
  6. **Ma trận Truy xuất Yêu cầu**: Ánh xạ trực tiếp từ `BAC-xx` / `FR-xx` trong `prd.md` sang Tiêu chí Nghiệm thu (`AC-ID`) và Kịch bản Test (`TC-ID`).

> 🛡️ **Quality Gate 1**: Duyệt `plan.md`. Không viết code khi chưa có hợp đồng chuẩn này.

---

### Giai đoạn 2: Thiết lập Rào Chắn Dòng Lệnh & Thư viện (Guardrails)
- **Kiểm soát Tập trung File Cấu hình Gốc**: Subagents không được tự ý sửa các file manifest (`pyproject.toml`, `package.json`, `docker-compose.yml`, `alembic.ini`) để triệt tiêu race condition trong `Workspace: "inherit"`. Khi cần thêm dependency, subagent chỉ cắm cờ `[DEPENDENCY REQUIRED]`. Độc quyền Tech Lead Orchestrator kiểm tra và cập nhật file manifest.
- Áp dụng quy chuẩn Sandbox: Không chạy `pip/npm install` trần khi không có mạng; cập nhật manifest và cắm cờ `[DEPENDENCY REQUIRED]`.
- Chạy smoke check Day-0: `.venv/bin/ruff check src/` để chắc chắn không có lỗi cú pháp tồn dư.

---

### Giai đoạn 3: Triển khai Lập trình Đợt kép (2-Wave Pipelined Execution)
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
- **Nhánh 1B - Frontend & Mobile Specialist (`frontend-dev` tại `src/frontend/` & `src/mobile/` — `Model: "inherit"`)**:
  - **Tùy chọn Khung làm việc (Framework Profiles)**:
    - *Profile 1 - Web Next.js 15 (Mặc định)*: Server Component-First, App Router (`app/`), Tailwind CSS, SSR + Client Components.
    - *Profile 2 - Web React Vite*: SPA Client-Side Rendering (`src/App.tsx`), Vite bundling siêu tốc, Tailwind CSS, Lucide icons.
    - *Profile 3 - Mobile React Native*: Expo SDK 51/52, Expo Router (`app/`), NativeWind v4 (Tailwind CSS Mobile), SafeAreaProvider.
    - *Công cụ chuyển đổi / kích hoạt*: `python scripts/setup_frontend.py` (`--status`, `--preset vite`, `--preset nextjs`, `--add-mobile`).
  - Tạo TypeScript types tại `src/frontend/src/types/` (và `src/mobile/src/types/` nếu có mobile) khớp 100% với Data Contract Matrix (`snake_case`, 0 `any`).
  - Tạo mock fixtures tại `mocks/` hỗ trợ `isMockMode()` và cờ `NEXT_PUBLIC_USE_MOCKS=true` (hoặc `VITE_USE_MOCKS=true`, `EXPO_PUBLIC_USE_MOCKS=true`).
  - Xây dựng UI components & screens xử lý trọn vẹn **4 trạng thái UI**: `Loading`, `Error`, `Empty`, `Success`.
  - **Universal Typed API Client**:
    - Phân giải URL tự động qua `getApiBaseUrl()` (hỗ trợ SSR `INTERNAL_API_URL`, Browser Next.js `NEXT_PUBLIC_API_URL`, Vite `VITE_API_URL`, và Mobile Expo `EXPO_PUBLIC_API_URL`).
    - Hỗ trợ Android emulator loopback: Tự động dùng `http://10.0.2.2:8000` thay cho `localhost` khi chạy trên Android.
    - Dọn dẹp cache an toàn: `clearClientApiCache()` (chống crash khi `sessionStorage`/`localStorage` vắng mặt trên Mobile).
  - Kiểm tra kiểu:
    - Web: `npm --prefix src/frontend run typecheck`
    - Mobile (nếu có): `npm --prefix src/mobile run typecheck`

#### Wave Handshake Gate, Cảnh Báo Lệch Schema Sớm & Tối Ưu Hóa Tiến Độ Pipelined:
1. **Báo cáo Bàn giao Chuẩn hóa từ `db-dev` (`[HANDSHAKE-HANDOVER]`)**:
   Ngay khi hoàn tất models, repositories và migrations trong `src/db/`, `db-dev` bắt buộc gửi báo cáo bàn giao chuẩn hóa cho Tech Lead:
   ```text
   [HANDSHAKE-HANDOVER]
   - Feature: <feature-slug>
   - Squad: db-dev
   - Models Created: <danh sách các models đã tạo trong src/db/models/>
   - Contract Modified: TRUE | FALSE
   - Contract Changes: <chi tiết các trường/cột thay đổi so với plan.md, hoặc NONE>
   - Status: READY_FOR_HANDSHAKE
   ```

2. **Kiểm tra Kỹ thuật Khách quan (Objective Smoke Check)**:
   Tech Lead Orchestrator thực hiện kiểm tra nhanh:
   ```bash
   python3 -m py_compile src/db/models/*.py
   .venv/bin/ruff check src/db/
   ```
   - Xác nhận `src/db/models/__init__.py` đã export các models mới sạch sẽ.
   - *Nếu phát hiện lỗi cú pháp hoặc import*: DỪNG LẠI, KHÔNG khởi chạy `backend-dev` mà gửi ngay `[SELF-HEALING ACTION REQUIRED]` qua `send_message` tới `SQUAD_REGISTRY["db-dev"]`.

3. **Cơ Chế Phân Luồng, Cảnh Báo Lệch Schema Sớm & Xử Lý Bất Đồng Bộ (Early Drift & Async Ingestion Protocol)**:
   - **Trường hợp A: `Contract Modified: FALSE` (Khớp 100% hợp đồng ban đầu)**:
     - Tech Lead **KÍCH HOẠT NGAY `backend-dev` (Wave 2)** mà không cần chờ `frontend-dev` xong 100%. Backend chạy gối đầu song song với Frontend giúp rút ngắn 25-40% tổng thời gian phát triển!
   - **Trường hợp B: `Contract Modified: TRUE` (Phát hiện Lệch Schema Sớm & Xử lý Bất đồng bộ)**:
     - *Bước B1 (Cập nhật Hợp đồng SSOT)*: Tech Lead cập nhật ngay `docs/specs/<feature-slug>/plan.md`:
       - Nâng version (ví dụ: `1.0.0` $\to$ `1.1.0`).
       - Cập nhật bảng **Cross-Layer Data Contract Matrix** và **REST API Contract** cho khớp với schema thực tế của `db-dev`.
     - *Bước B2 (Cảnh báo sớm Bất đồng bộ cho Frontend — Non-blocking Dispatch)*: Tech Lead gửi ngay thông điệp `[CONTRACT-UPDATE NOTICE]` qua `send_message` tới `SQUAD_REGISTRY["frontend-dev"]` (vốn đang chạy song song):
       ```text
       [CONTRACT-UPDATE NOTICE]
       - Feature: <feature-slug>
       - Version: 1.1.0
       - Source: db-dev schema adjustment at Handshake Gate
       - Changes: <chi tiết các trường/cột thay đổi>
       - Action Required: Hoàn tất tác vụ nguyên tử dở dang hiện tại (nếu có), sau đó cập nhật lại TypeScript types tại src/frontend/src/types/ và mock fixtures tại src/frontend/src/lib/api/mocks/ theo plan.md v1.1.0. Sau khi hoàn tất, phản hồi [CONTRACT-ALIGNED].
       ```
       *Cơ chế Tiếp nhận Bất đồng bộ của Antigravity 2.0*: Nếu `frontend-dev` đang bận thực thi một lệnh/tool call, Antigravity bảo toàn tính toàn vẹn (non-preemptive). `frontend-dev` hoàn thành thao tác hiện tại, tự động nhận thông báo tại lượt tiếp theo để đồng bộ types/mocks và phản hồi `[CONTRACT-ALIGNED]`.
     - *Bước B3 (Khởi chạy Backend Không Chờ Đợi — Pipelined Overlap)*: Tech Lead **KHÔNG CẦN CHỜ** `frontend-dev` phản hồi `[CONTRACT-ALIGNED]` mới khởi chạy `backend-dev`! Tech Lead kích hoạt ngay `backend-dev` (Wave 2) bám sát theo `plan.md` v1.1.0. Cả Backend và Frontend cùng tiến hành song song hướng về cùng hợp đồng v1.1.0 mà không bên nào bị nghẽn (zero blocking).
     - *Bước B4 (`frontend-dev` đồng bộ & phản hồi)*: `frontend-dev` đồng bộ types/mocks và gửi phản hồi:
       ```text
       [CONTRACT-ALIGNED]
       - Feature: <feature-slug>
       - Version: 1.1.0
       - Squad: frontend-dev
       - Updated Files: src/frontend/src/types/..., src/frontend/src/lib/api/mocks/...
       - Status: ALIGNED_WITH_CONTRACT_V1.1.0
       ```
     - *Bước B5 (Chốt Hội Tụ Trước QA — Pre-QA Wave Convergence Gate)*: Trước khi chuyển sang Giai đoạn 4 (QA Testing), Tech Lead chốt hội tụ: chỉ chuyển `NEXT_PUBLIC_USE_MOCKS=false` và kích hoạt `qa-tester` khi CẢ HAI squad đều gửi xác nhận hoàn tất (`backend-dev` xong live API và `frontend-dev` đã gửi `[CONTRACT-ALIGNED]`). Toàn bộ 3 tầng DB - Backend - Frontend được đồng bộ tuyệt đối, triệt tiêu 100% rủi ro lệch hợp đồng khi vào kiểm thử.

#### Đợt 2 (Wave 2 - Kết nối Backend & Đồng bộ Live API):
- **Backend Specialist (`backend-dev` tại `src/backend/` — `Model: "inherit"`)**:
  - Kích hoạt ngay sau khi vượt qua Wave Handshake Gate, Tech Lead lưu lại `conv_id_be`. Chạy gối đầu song song với `frontend-dev`.
  - Viết Pydantic v2 schemas tại `src/backend/app/schemas/` (`ConfigDict(from_attributes=True)`, giới hạn `max_length`, `ge`/`le`).
  - Viết Services xử lý business logic và transaction tại `src/backend/app/services/`.
  - Viết API routers tại `src/backend/app/api/v1/endpoints/` kết nối models trực tiếp từ `src/db/` thông qua `PYTHONPATH=src`. Expose cả `/health` và `/api/v1/health`.
  - Cắm router vào `api_router` tập trung tại `src/backend/app/api/v1/router.py`.
  - **Đồng bộ Mock → Live API & Cache Invalidation**:
    - Khi cả `backend-dev` và `frontend-dev` hoàn tất, chuyển `NEXT_PUBLIC_USE_MOCKS=false` trong `.env`.
    - Typed API Client trong `src/frontend/src/lib/api/client.ts` tự động áp dụng `cache: 'no-store'`, header `Cache-Control: 'no-cache'`, và gọi `clearClientApiCache()` để xóa sạch stale cache cả ở Storage và Browser CacheStorage.
    - Chạy script kiểm tra mạng nhanh: `.venv/bin/python scripts/verify_network.py`.

---

### Giai đoạn 4: Kiểm thử Tự động & Vòng lặp Sửa lỗi (`qa-tester`)
- `qa-tester` đối chiếu `plan.md` và viết test tự động tại `src/backend/tests/test_<feature>.py`.
- **Quy Chuẩn Kiểm Thử Kiểu Dữ Liệu PostgreSQL Nâng Cao (Cross-DB Testing)**:
  - Khi test các tính năng đặc thù PostgreSQL (`pgvector`, `tsvector`, native enum, array operators), gắn decorator `@pytest.mark.postgres_only`.
  - SQLite in-memory test mặc định sẽ tự động skip an toàn các test này mà không báo `FAILED`.
  - Khi có PostgreSQL: `TEST_DATABASE_URL=postgresql+asyncpg://... python -m pytest src/backend/tests src/db/tests -v`.
- Thực thi chuỗi lệnh kiểm tra (5 tầng toàn diện — Đa nền tảng):
  - **Khuyên dùng (1-Click Tự động trên mọi HĐH)**:
    ```bash
    python scripts/smoke_test.py
    ```
  - **Windows (PowerShell / CMD)**:
    ```powershell
    .\.venv\Scripts\python.exe -m ruff check src/
    python scripts/verify_contracts.py <feature-slug>
    python scripts/verify_migrations.py
    .\.venv\Scripts\python.exe -m pytest src/backend/tests src/db/tests -v
    npm --prefix src/frontend run typecheck
    npm --prefix src/mobile run typecheck # (Nếu kích hoạt Mobile App)
    ```
  - **Linux / macOS**:
    ```bash
    .venv/bin/python -m ruff check src/
    python scripts/verify_contracts.py <feature-slug>
    python scripts/verify_migrations.py
    .venv/bin/python -m pytest src/backend/tests src/db/tests -v
    npm --prefix src/frontend run typecheck
    npm --prefix src/mobile run typecheck # (Nếu kích hoạt Mobile App)
    ```
- **Khởi Động Server & Kiểm Thử Trực Quan Giao Diện 4 Trạng Thái UI (Visual Verification qua `/browser`)**:
  - Đối với các tính năng có giao diện Web hoặc Mobile (`src/frontend/` hoặc `src/mobile/`), QA Tester kết hợp kiểm tra typecheck với việc thẩm định trực quan đủ 4 trạng thái UI:
    1. *Loading State*: Skeleton loader / Spinner hiển thị chống layout shift (CLS).
    2. *Empty State*: Thông điệp thân thiện + Nút kêu gọi hành động (CTA) khi dữ liệu rỗng.
    3. *Error State*: Banner cảnh báo đỏ + Nút "Thử lại" (Retry) khi API lỗi.
    4. *Success State*: Dữ liệu hiển thị chuẩn xác, bố cục responsive Desktop (1280px) & Mobile (375px).
  - Khởi động dev server bằng lệnh:
    ```bash
    python scripts/start_dev.py           # Chạy song song FastAPI & Frontend
    # hoặc kiểm tra trạng thái cổng: python scripts/start_dev.py --check
    ```
  - Khuyến nghị kích hoạt phím tắt `/browser http://localhost:3000/<route>` trên chat Antigravity 2.0 để tương tác trực quan, chụp ảnh màn hình và đối chiếu AC.
- Xuất báo cáo tại `docs/specs/<feature-slug>/test-report.md` (kèm Chỉ số Metrics, Bảng Kiểm Định Trực Quan Mục 2.2 và Structured Bug Tickets).
- **Vòng lặp Self-Healing (Tự sửa lỗi) & Bảo Toàn Ngữ Cảnh (Context Preservation)**:
  - Nếu `overall_status: FAILED`:
    - **Bảo toàn Ngữ cảnh**: Tech Lead **BẮT BUỘC dùng `send_message`** gửi yêu cầu sửa lỗi tới Conversation ID của squad (`SQUAD_REGISTRY[target_agent]`). TUYỆT ĐỐI KHÔNG gọi `invoke_subagent` mới.
    - **Quy chuẩn Cắt tỉa Nhật ký Lỗi Chống Phình Ngữ Cảnh (Anti-Bloat Traceback Rule)**:
      Tech Lead TUYỆT ĐỐI KHÔNG copy-paste toàn bộ output log của terminal. Chỉ trích xuất đúng **15-25 dòng trọng tâm nhất** mô tả chính xác điểm gãy (dòng file, loại ngoại lệ, assertion failure).
    - Dev Squad sửa lỗi trong thư mục phân quyền, chạy smoke test và gửi phản hồi `[FIX-COMPLETED]` (tóm tắt súc tích trong 3-5 gạch đầu dòng).
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

### Giai đoạn 6: Đóng gói, Git Commit & Dọn Dẹp Subagent (Tech Lead Orchestrator)
1. Rà soát `git status --short`. Nếu có cờ `[DEPENDENCY REQUIRED]`, Tech Lead Orchestrator trực tiếp cập nhật `pyproject.toml` hoặc `src/frontend/package.json`.
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
3. **Tự Động Hóa Dọn Dẹp Subagent (Subagent Lifecycle Cleanup)**:
   - Sau khi commit thành công, Tech Lead Orchestrator **tự động gọi công cụ `manage_subagents` với `Action: "kill"`** cho toàn bộ Conversation IDs trong `SQUAD_REGISTRY` (hoặc `Action: "kill_all"`).
   - *Mục đích*: Giải phóng hoàn toàn RAM/CPU và background workers của Antigravity 2.0, ngăn ngừa rò rỉ (leak) subagent hoặc context zombie sang các tính năng tiếp theo.
4. Bàn giao cho User: Cung cấp Commit Hash, danh sách files, tài liệu trong `docs/specs/<feature-slug>/`, hướng dẫn kiểm chứng tính năng và xác nhận dọn dẹp subagents hoàn tất.

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

---

## 7. Cẩm Nang Slash Commands Dành Cho Người Dùng (Antigravity 2.0 Shortcuts)

Trên giao diện Antigravity 2.0, **Slash Commands** là các phím tắt trực tiếp trên khung chat giúp người dùng (Product Owner / Developer) kích hoạt các chế độ tư duy và quy trình tự động hóa chuyên sâu. Tác tử AI không thể tự gõ lệnh này, nhưng Tech Lead Orchestrator sẽ chủ động gợi ý cho bạn sử dụng khi phù hợp với bối cảnh tác vụ.

### 7.1. Bảng Ma Trận Ánh Xạ Slash Commands Theo Giai Đoạn Dự Án

| Lệnh Slash | Khi Nào Nên Sử Dụng? | Giai Đoạn Đội Dev Tương Ứng | Tác Dụng Cụ Thể Lên Hệ Thống |
| :--- | :--- | :--- | :--- |
| **`/grill-me`** | Bắt đầu ý tưởng mới, cần làm rõ phạm vi, phân quyền và quy tắc nghiệp vụ rẽ nhánh | **Giai đoạn 0: BA Agent (`ba`)** | Kích hoạt phiên phỏng vấn tương tác chuyên sâu. BA Agent sẽ chất vấn có cấu trúc để làm rõ các giả định ngầm, edge cases trước khi chốt `prd.md`. |
| **`/plan`** | Khi tính năng phức tạp, cần phân tích kiến trúc đa tầng trước khi viết mã | **Giai đoạn 1: Planner (`planner`)** | Yêu cầu hệ thống lập kế hoạch chi tiết từng bước, khảo sát mã nguồn hiện hữu và hoàn thiện Ma trận hợp đồng 3 tầng `plan.md`. |
| **`/goal`** | Cần triển khai trọn vẹn một tính năng từ A $\to$ Z (chạy qua đêm / không ngắt quãng) | **Giai đoạn 3 $\to$ 6: Full Pipeline** | Đặt mục tiêu bền bỉ: Đội Dev tự động phối hợp qua 2 Wave, tự sửa lỗi qua QA & Review, không dừng lại cho đến khi đạt 100% test passed & review approved. |
| **`/boost`** | Bài toán thuật toán khó, thiết kế module cốt lõi, hoặc refactor kiến trúc lớn | **Giai đoạn 1 & 4 (Kiến trúc & Review)** | Kích hoạt chế độ Deep Thinking với mô hình mạnh nhất (`pro`), phân tích đa chiều và kiểm chứng nghiêm ngặt để đưa ra giải pháp tối ưu. |
| **`/teamwork-preview`**| Trước khi bắt đầu một Epic lớn, muốn xem trước cách các subagents phối hợp | **Trước Giai đoạn 2 (Dev Squads)** | Trực quan hóa sơ đồ phối hợp, phân vai trò, quyền hạn thư mục và luồng chuyển giao dữ liệu giữa các thành viên trong đội. |
| **`/learn`** | Khi bạn vừa hướng dẫn AI một quy tắc mới hoặc vừa sửa một lỗi môi trường đặc thù | **Sau khi xử lý sự cố / Customization** | Yêu cầu Antigravity ghi nhớ vĩnh viễn kinh nghiệm hoặc quy tắc này vào tri thức workspace cho các phiên làm việc tiếp theo. |
| **`/browser`** | Cần kiểm tra giao diện trực quan trên trình duyệt thực tế, audit 4 trạng thái UI, responsive mobile/desktop | **Giai đoạn 4: QA Testing & UI Audit** | Kích hoạt trình duyệt duyệt trang đích (`http://localhost:3000/...`), chụp ảnh màn hình, kiểm thử 4 trạng thái UI (Loading/Empty/Error/Success) và A11y. |
| **`/schedule`** | Cần hẹn giờ hoặc đặt lịch chạy kiểm thử, smoke test, kiểm tra schema định kỳ | **Bảo trì / Giám sát liên tục** | Thiết lập bộ đếm một lần hoặc cron job định kỳ trong nền (ví dụ: chạy test kiểm tra drift mỗi sáng). |

### 7.2. Kịch Bản Sử Dụng Điển Hình (Practical Scenarios)

1. **Khởi động một Phân hệ Mới với BA & Bóc tách Epic**:
   * *Người dùng gõ*: `/grill-me Hãy cùng tôi thiết lập tính năng Quản lý Đơn hàng (Order Management)`
   * *Hiệu ứng*: BA Agent lập tức phân tích quy mô Epic, bóc tách thành các lát cắt nguyên tử (e.g. `order-checkout` -> `order-payment`), đặt các câu hỏi trọng tâm P0 về luồng trạng thái đơn hàng, phương thức thanh toán và phân quyền, sau đó xuất bản `docs/specs/order-management/prd.md`.

2. **Chạy Tự Động Xuyên Suốt Tính Năng Đến Khi Bàn Giao**:
   * *Người dùng gõ*: `/goal Triển khai hoàn chỉnh tính năng order-management theo prd.md đã duyệt`
   * *Hiệu ứng*: Tech Lead kích hoạt Planner $\to$ Wave 1 (DB + Frontend) $\to$ Wave 2 (Backend) $\to$ QA Tester (Self-Healing) $\to$ Code Reviewer $\to$ Git Commit. Đội dev kiên trì tự sửa lỗi cho đến khi hoàn tất 100%.

3. **Ghi Nhớ Quy Chuẩn Dự Án Đặc Thù**:
   * *Người dùng gõ*: `/learn Hãy luôn sử dụng asyncpg pool với Transaction Mode port 6543 cho FastAPI runtime và Session Mode port 5432 cho Alembic migrations`
   * *Hiệu ứng*: Antigravity lưu quy chuẩn này vào cấu hình workspace, đảm bảo mọi subagent trong tương lai luôn tuân thủ chính xác.

4. **Kiểm Tra Trực Quan Giao Diện & 4 Trạng Thái UI**:
   * *Người dùng gõ*: `/browser http://localhost:3000/orders Kiểm tra 4 trạng thái UI Loading, Empty, Error, Success và độ co giãn mobile 375px`
   * *Hiệu ứng*: Antigravity mở trình duyệt truy cập route chỉ định, tương tác với các nút bấm, chụp ảnh màn hình kiểm chứng và hỗ trợ QA Tester đối chiếu trực quan với AC.

