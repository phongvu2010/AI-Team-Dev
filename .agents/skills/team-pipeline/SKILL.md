---
name: team-pipeline
description: >-
  Orchestrates the Multi-Agent Matrix Dev Team pipeline (BA [Elicitation & PRD] -> Planner -> [Wave 1: DB Dev + Frontend Dev -> Wave 2: Backend Dev] -> QA Tester -> Code Reviewer) on Antigravity 2.0. Activate this skill when the user wants to build a full-stack feature, run the multi-agent team workflow, or coordinate tasks across DB, Backend, and Frontend teams.
---

# Multi-Agent Matrix Dev Team Pipeline (`team-pipeline`)

Skill này cung cấp quy trình điều phối chuẩn (Runbook), cơ chế phản hồi tự động (**Feedback Loop & Circuit Breaker**), phòng chống lệch chuẩn hợp đồng (**Contract Desync Prevention**), rào chắn an toàn dòng lệnh (**CLI Guardrails**) và bộ mẫu tài liệu bàn giao (**Artifact Handover Schema**) cho mô hình **Ma trận (Matrix Architecture)** trên Antigravity 2.0.

---

## 1. Sơ Đồ Luồng Thực Thi & Tài Liệu Bàn Giao (Artifact Handover Pipeline)

Mọi tính năng đều được định danh bằng `<feature-slug>` (`kebab-case`) và lưu trữ hồ sơ kỹ thuật tại `docs/specs/<feature-slug>/`:

| Giai đoạn | Subagent | Đầu vào (Input) | Đầu ra (Output Artifact & Code) | Handoff Template |
| :--- | :--- | :--- | :--- | :--- |
| **0. BA & Requirements** | `ba` | Prompt / Yêu cầu ban đầu từ User | `docs/specs/<feature-slug>/prd.md` (FRs, Business Rules, Edge Cases, BACs, Clarification Log) | [prd-template.md](./resources/prd-template.md) |
| **1. Planning** | `planner` | `prd.md` (đã duyệt) + Codebase hiện tại | `docs/specs/<feature-slug>/plan.md` (Metadata + Data Contract Matrix + API Spec + UI Spec + AC Matrix) | [plan-template.md](./resources/plan-template.md) |
| **2A. Wave 1 (DB)** | `db-dev` | `plan.md` (Data Contract) | Code trong `src/db/` (SQLAlchemy 2.0 Models, Repositories, Migrations, Seeds) | - |
| **2B. Wave 1 (Frontend)** | `frontend-dev` | `plan.md` (API Contract + UI Spec) | Code trong `src/frontend/` (TypeScript Types, API Client, Mock Fixtures, 4 UI States) | - |
| **2C. Wave 2 (Backend)** | `backend-dev` | `plan.md` (API Contract) + `src/db/` | Code trong `src/backend/` (Pydantic v2 Schemas, Services, Routers kết nối `src/db/`) | - |
| **3. Testing & Feedback** | `qa-tester` | `plan.md` + Code trong `src/` | Linter + Pytest SQLite Memory + Typecheck + `docs/specs/<feature-slug>/test-report.md` (Bug Tickets) | [test-report-template.md](./resources/test-report-template.md) |
| **4. Review & Audit** | `code-reviewer` | `plan.md` + `test-report.md` + `git diff` | Audit `git diff` + `docs/specs/<feature-slug>/review-report.md` (Quality Scorecard & Findings) | [review-report-template.md](./resources/review-report-template.md) |
| **5. Packaging** | `tech-lead` | `review-report.md` (`APPROVED`) + Git status | Conventional Git commit + Handoff report cho User | - |

---

## 2. Rào Chắn An Toàn Dòng Lệnh (CLI Execution Guardrails)

Nhằm đảm bảo tính cô lập và toàn vẹn của hệ thống, mọi tác tử phải tuân thủ nghiêm ngặt:

### 2.1. Whitelist theo vai trò:
- **`ba`**: Sử dụng `ask_question` để phỏng vấn/làm rõ yêu cầu với User, và các công cụ đọc/ghi tài liệu (`view_file`, `write_to_file`, `replace_file_content`). Tuyệt đối không can thiệp mã nguồn hay chạy lệnh shell.
- **`planner`**: Chỉ thao tác đọc/ghi file tài liệu (`view_file`, `write_to_file`, `replace_file_content`).
- **`db-dev`**: Chỉ chạy `.venv/bin/ruff check src/db/`, `python3 -m py_compile src/db/...`, `PYTHONPATH=src .venv/bin/python src/db/migrations/generate_offline_migration.py <slug>`, `alembic ...`, `PYTHONPATH=src .venv/bin/python src/db/seeds/runner.py`.
- **`backend-dev`**: Chỉ chạy `.venv/bin/ruff check src/backend/`, `python3 -m py_compile src/backend/...`.
- **`frontend-dev`**: Chỉ chạy `npm --prefix src/frontend run typecheck`, `npm --prefix src/frontend run lint`, `npm --prefix src/frontend run build`.
- **`qa-tester`**: Chỉ chạy `.venv/bin/ruff check src/`, `PYTHONPATH=src ./.venv/bin/pytest src/backend/tests -v`, `npm --prefix src/frontend run typecheck`.
- **`code-reviewer`**: Chỉ chạy `git status --short`, `git diff --stat`, `git diff -- src/ docs/ ':!*package-lock.json' ':!*.lock' ':!*.min.*'`, `git diff`.
- **`tech-lead`**: Điều phối subagents, quản lý và dọn dẹp subagents qua `manage_subagents`, độc quyền cập nhật manifest cấu hình gốc (`pyproject.toml`, `package.json`), git add, git commit.

### 2.2. Blacklist tuyệt đối:
- Cấm `rm -rf` ngoài thư mục tạm, `git reset --hard`, `git clean -fdx`, `git checkout .`, `git push --force`.
- Cấm subagents tự ý sửa đổi file cấu hình gốc (`pyproject.toml`, `docker-compose.yml`, `alembic.ini`, `src/frontend/package.json`). Khi cần thêm thư viện mới, subagent BẮT BUỘC chỉ cắm cờ `[DEPENDENCY REQUIRED]`. Độc quyền Tech Lead Orchestrator chỉnh sửa các file manifest này.
- Cấm chạy `pip install` hoặc `npm install` trần trong sandbox.
- Cấm gọi `pytest`, `ruff`, `python` trần không trỏ vào `.venv/bin/`.
- Cấm tác tử sửa file ngoài thư mục phụ trách (`src/db/` cho db-dev, `src/backend/` cho backend-dev, `src/frontend/` cho frontend-dev).

---

## 3. Quy Trình Điều Phối Chi Tiết Cho Tech Lead (Main Agent)

### Bước 0: Khởi chạy `ba` & Làm rõ yêu cầu, Thiết lập PRD (Requirements Elicitation & PRD Gate)
Gọi `invoke_subagent`:
- `TypeName`: `"ba"`
- `Role`: `"Business Analyst & Requirements Engineer"`
- `Model`: `"pro"` *(Model Pro đảm bảo tư duy phân tích nghiệp vụ sắc bén, phát hiện điểm mù và thiết lập kịch bản phỏng vấn)*
- `Prompt`: Phân tích prompt ban đầu từ User, sử dụng `ask_question` để phỏng vấn các điểm mơ hồ, xác định phạm vi In-Scope/Out-of-Scope, Business Rules, Edge Cases, User Journeys, và Business Acceptance Criteria. Xuất bản PRD tại `docs/specs/<feature-slug>/prd.md` theo mẫu `.agents/skills/team-pipeline/resources/prd-template.md`.
- **Cổng Nghiệm Thu PRD (PRD Sign-off Gate)**:
  - `ba` trình bày tóm tắt cho User và xin phê duyệt (Sign-off).
  - Khi User chấp thuận, tài liệu được gắn `status: APPROVED_BY_USER`.
  - Tech Lead kiểm tra xác nhận sự phê duyệt này trước khi chuyển sang Bước 1.

### Bước 1: Khởi chạy `planner` & Chuyển hóa PRD thành Hợp đồng Kỹ thuật
Gọi `invoke_subagent`:
- `TypeName`: `"planner"`
- `Role`: `"System Architect & Planner"`
- `Model`: `"pro"` *(Model Pro đảm bảo khả năng tổng hợp kiến trúc sâu và ma trận dữ liệu 3 tầng)*
- `Prompt`: Đọc kỹ tài liệu PRD đã được phê duyệt tại `docs/specs/<feature-slug>/prd.md`, đọc mẫu `.agents/skills/team-pipeline/resources/plan-template.md`, khảo sát hiện trạng `src/` và tạo bản thiết kế đầy đủ tại `docs/specs/<feature-slug>/plan.md`.
- **Yêu cầu bắt buộc**:
  - Ánh xạ trực tiếp từ `BAC-xx` / `FR-xx` trong PRD sang `AC-xx` (Technical Acceptance Criteria) và `TC-xx` (Test Case ID).
  - Thiết lập bảng **Cross-Layer Data Contract Matrix**: Thống nhất 100% tên trường `snake_case` giữa DB Column, Pydantic Schema và TypeScript Interface.
  - Chuẩn hóa kiểu dữ liệu: UUID (Python `uuid.uuid4`), Timestamps (ISO 8601 UTC), Arrays (`JSON` default list).
  - Cung cấp Wave 1 Mock Fixtures cho Frontend.
  - Ma trận truy xuất Acceptance Criteria (`AC-ID` -> `TC-ID`).

### Bước 2: Khởi chạy Đội ngũ Dev theo Quy trình 2-Wave + Wave Handshake Gate
- **Chiến lược Workspace Mode (`Workspace: "inherit"`)**:
  - Khi gọi `invoke_subagent` cho các Dev Squads, bắt buộc đặt `"Workspace": "inherit"`. Vì `db-dev` (`src/db/`), `frontend-dev` (`src/frontend/`) và `backend-dev` (`src/backend/`) thao tác trên các thư mục độc lập tuyệt đối, việc kế thừa workspace loại bỏ xung đột Git và giúp Wave 2 cùng QA nhìn thấy code ngay lập tức mà không cần merge branch.
- **Quản lý Định danh Hội thoại (Squad Conversation Registry)**:
  - Tech Lead **BẮT BUỘC lưu lại Conversation ID** của từng Dev Squad:
    `SQUAD_REGISTRY = {"db-dev": conv_id_db, "frontend-dev": conv_id_fe, "backend-dev": conv_id_be}`
  - Registry này dùng để định tuyến toàn bộ thông điệp sửa lỗi trong vòng đời tính năng qua `send_message`.
- **Wave 1 (Triển khai song song `db-dev` & `frontend-dev`)**:
  - Gọi đồng thời `db-dev` (`Model: "inherit"`) và `frontend-dev` (`Model: "inherit"`) trong cùng lệnh `invoke_subagent`.
  - `db-dev` xây dựng models (kế thừa `UUIDPrimaryKeyMixin`, mảng dùng `JSON`), repositories async (dùng `selectinload`), migrations (dùng `DIRECT_DATABASE_URL` port 5432 nếu có Supabase, hoặc `generate_offline_migration.py` nếu không có PostgreSQL) và seeds tại `src/db/`.
  - `frontend-dev` xây dựng TypeScript types, API client wrapper, mock fixtures và UI components xử lý đủ 4 trạng thái (Loading, Error, Empty, Success) tại `src/frontend/` (hỗ trợ `isMockMode()` với cờ `NEXT_PUBLIC_USE_MOCKS=true` để phát triển và kiểm chứng UI độc lập).
- **Wave Handshake Gate, Cảnh Báo Lệch Schema Sớm & Tối Ưu Hóa Tiến Độ Pipelined**:
  - `db-dev` khi xong Wave 1 bắt buộc gửi thông điệp `[HANDSHAKE-HANDOVER]` kèm cờ `Contract Modified: TRUE | FALSE`.
  - Tech Lead kiểm tra chéo:
    ```bash
    python3 -m py_compile src/db/models/*.py
    .venv/bin/ruff check src/db/
    ```
  - Xác nhận models compile sạch sẽ và được export đầy đủ tại `src/db/models/__init__.py`. Nếu có lỗi cú pháp, gửi ngay `[SELF-HEALING ACTION REQUIRED]` qua `send_message` tới `SQUAD_REGISTRY["db-dev"]`.
  - **Cơ chế Cảnh báo Lệch Schema Sớm & Xử Lý Bất Đồng Bộ (Early Drift & Async Ingestion Protocol)**:
    - **Nếu `Contract Modified: FALSE`**: Models khớp 100% với `plan.md`. Tech Lead **KÍCH HOẠT NGAY `backend-dev` (Wave 2)** mà không cần chờ `frontend-dev` xong 100%. Backend chạy gối đầu song song với Frontend (Pipelined Wave Execution) giúp rút ngắn 25-40% tổng thời gian phát triển!
    - **Nếu `Contract Modified: TRUE`**:
      1. Tech Lead cập nhật ngay `docs/specs/<feature-slug>/plan.md`, nâng `version` (`1.0.0` $\to$ `1.1.0`), đồng bộ lại **Cross-Layer Data Contract Matrix** và **API Contract**.
      2. Tech Lead gửi ngay thông điệp `[CONTRACT-UPDATE NOTICE]` qua `send_message` tới `SQUAD_REGISTRY["frontend-dev"]` (bất đồng bộ phi chặn). `frontend-dev` hoàn thành thao tác nguyên tử hiện tại, tiếp nhận thông báo ở turn kế tiếp, cập nhật types/mocks và phản hồi `[CONTRACT-ALIGNED]`.
      3. Tech Lead **KHÔNG CẦN CHỜ** Frontend mà kích hoạt ngay `backend-dev` (Wave 2) bám sát theo `plan.md` v1.1.0 (zero blocking).
      4. **Chốt Hội Tụ Trước QA (Pre-QA Wave Convergence Gate)**: Trước khi chuyển sang Bước 3 (QA Testing), Tech Lead chốt hội tụ: chỉ chuyển `NEXT_PUBLIC_USE_MOCKS=false` và kích hoạt `qa-tester` khi CẢ HAI squad đều hoàn thành (`backend-dev` xong live API và `frontend-dev` đã gửi `[CONTRACT-ALIGNED]`). Triệt tiêu 100% rủi ro lệch hợp đồng.
- **Wave 2 (Triển khai `backend-dev` gối đầu song song & Đồng bộ Live API)**:
  - Gọi `backend-dev` (`Model: "inherit"`) trong `invoke_subagent` và ghi nhận `conv_id_be`.
  - `backend-dev` tạo Pydantic v2 schemas (`ConfigDict(from_attributes=True)`), services nghiệp vụ và API routers tại `src/backend/`, kết nối trực tiếp với models từ `src/db/` qua `PYTHONPATH=src`.
  - **Đồng bộ Mock → Live API & Cache Invalidation**: Khi cả `backend-dev` và `frontend-dev` đều hoàn tất, chuyển `NEXT_PUBLIC_USE_MOCKS=false`. Typed API client tự động áp dụng `cache: 'no-store'`, header `Cache-Control: 'no-cache'`, và gọi `clearClientApiCache()` để xóa sạch cache mock cũ.

### Bước 3: Khởi chạy `qa-tester` & Vòng lặp Tự sửa lỗi (Self-Healing Loop)
Gọi `invoke_subagent` với `TypeName: "qa-tester"`, `Model: "flash"`:
- *(Dùng Model Flash giúp hoàn thành chuỗi CLI linter/tests nhanh hơn 60% và tiết kiệm token)*.
- `qa-tester` chạy chuỗi kiểm tra:
  1. `.venv/bin/ruff check src/`
  2. `PYTHONPATH=src ./.venv/bin/pytest src/backend/tests -v`
     *(Mặc định chạy SQLite in-memory cô lập. Các bài test có tính năng đặc thù PostgreSQL được gắn `@pytest.mark.postgres_only` sẽ tự động skip an toàn khi chạy trên SQLite)*.
  3. `npm --prefix src/frontend run typecheck`
- Xuất báo cáo theo mẫu `.agents/skills/team-pipeline/resources/test-report-template.md` tại `docs/specs/<feature-slug>/test-report.md`.
- **Vòng lặp Self-Healing (Tự sửa lỗi) & Bảo Toàn Ngữ Cảnh (Context Preservation)**:
  - Nếu `overall_status: FAILED`:
    - **Bảo toàn Ngữ cảnh**: Tech Lead **BẮT BUỘC sử dụng `send_message`** gửi yêu cầu sửa lỗi tới Conversation ID của squad liên quan (`SQUAD_REGISTRY[target_agent]`).
    - **TUYỆT ĐỐI KHÔNG** gọi `invoke_subagent` tạo mới agent cho cùng squad trong vòng lặp Self-Healing. Tái sử dụng Conversation ID giúp Subagent duy trì 100% ngữ cảnh (working memory, code context, terminal logs), giảm 70% token tiêu hao và sửa lỗi chính xác gấp 3 lần.
    - *Ngoại lệ*: Chỉ khi `send_message` gặp lỗi (agent đã terminated/crashed) mới gọi `invoke_subagent` khởi tạo agent mới kèm tóm tắt ngữ cảnh.
    - Mẫu thông điệp điều phối:
      ```text
      [SELF-HEALING ACTION REQUIRED]
      - Feature: <feature-slug>
      - Iteration: <iteration_number> / 3
      - Target Agent: db-dev (src/db/) | backend-dev (src/backend/) | frontend-dev (src/frontend/)
      - Target File & Line: <đường_dẫn_file>#L...
      - Failed Test ID: <mã test case hoặc tên hàm test>
      - Diagnostics & Traceback:
        <chi tiết lỗi trích từ Mục 4 test-report.md>
      - Reproduction Command: <lệnh tái hiện lỗi>
      - Instructions: Phân tích nguyên nhân và khắc phục triệt để trong thư mục phân quyền. Chạy smoke test và gửi báo cáo [FIX-COMPLETED] khi hoàn tất.
      ```
    - Dev Squad sửa lỗi và phản hồi lại bằng thông điệp `[FIX-COMPLETED]`:
      ```text
      [FIX-COMPLETED]
      - Feature: <feature-slug>
      - Iteration: <iteration_number>
      - Target Agent: <tên_agent>
      - Modified Files: <danh sách files đã sửa>
      - Contract Modified: TRUE | FALSE
      - Contract Changes: <chi tiết thay đổi schema/endpoint nếu TRUE, hoặc NONE>
      - Resolved Bug IDs: <BUG-01, ...>
      - Summary of Fix: <tóm tắt ngắn gọn giải pháp>
      ```
    - **Contract Drift Protection**: Nếu `Contract Modified: TRUE`, Tech Lead cập nhật `docs/specs/<feature-slug>/plan.md`, nâng `version` (e.g. `1.1.0`), đồng bộ lại Cross-Layer Data Contract Matrix và gửi thông báo cho squad liên quan qua `send_message`.
    - Tech Lead yêu cầu `qa-tester` chạy lại bài test. Tăng `iteration` thêm 1.
    - **Cơ chế Ngắt Mạch (Circuit Breaker)**: Tối đa **3 lần lặp**. Nếu quá 3 lần vẫn thất bại, tạm dừng và báo cáo sự cố cho User.

### Bước 4: Khởi chạy `code-reviewer` & Vòng lặp Phản hồi Review
Khi `test-report.md` đạt `PASSED 100%`:
- Gọi `invoke_subagent` với `TypeName: "code-reviewer"`, `Model: "pro"`.
- *(Dùng Model Pro để phân tích chuyên sâu các lỗ hổng bảo mật OWASP, N+1 query và Data Contract Alignment)*.
- `code-reviewer` thực thi **Token-Optimized Audit Protocol**:
  1. `git status --short` quét nhanh các file mới và sửa đổi.
  2. `git diff --stat` đo lường quy mô thay đổi.
  3. `git diff -- src/ docs/ ':!*package-lock.json' ':!*.lock' ':!*.min.*'` loại trừ lockfiles/minified files, dồn 100% token budget vào logic nghiệp vụ và 5 tiêu chí Quality Gate.
  4. Chấm điểm Quality Gate Scorecard và xuất `docs/specs/<feature-slug>/review-report.md`.
- **Vòng lặp Phản hồi Review (Review Feedback Loop) & Bảo Toàn Ngữ Cảnh**:
  - Nếu Verdict là `CHANGES_REQUESTED` (có lỗi `[CRITICAL]` hoặc `[MAJOR]`):
    - Tech Lead **BẮT BUỘC sử dụng `send_message`** gửi thông điệp tới `SQUAD_REGISTRY[target_agent]`, KHÔNG gọi mới `invoke_subagent`.
      ```text
      [REVIEW-FIX ACTION REQUIRED]
      - Feature: <feature-slug>
      - Iteration: <iteration_number> / 3
      - Target Agent: db-dev (src/db/) | backend-dev (src/backend/) | frontend-dev (src/frontend/)
      - Finding ID: <REV-01, ...>
      - Severity: [CRITICAL] | [MAJOR]
      - Target File & Line: <đường_dẫn_file>#L...
      - Issue Description & Diff:
        <mô tả và code diff từ Mục 3 review-report.md>
      - Remediation Guidance: <hướng dẫn sửa của reviewer>
      - Instructions: Khắc phục đúng các điểm vi phạm trên trong thư mục phân quyền. Chạy smoke test và gửi báo cáo [FIX-COMPLETED] khi hoàn tất.
      ```
    - Dev Squad sửa lỗi và gửi `[FIX-COMPLETED]`. Nếu `Contract Modified: TRUE`, Tech Lead cập nhật `plan.md`.
    - Tech Lead yêu cầu `qa-tester` chạy lại bài test để chống lỗi hồi quy (regression), sau đó yêu cầu `code-reviewer` thẩm định lại. Tối đa 3 vòng lặp.
  - Khi Verdict đạt `APPROVED`, chuyển sang Bước 5.

### Bước 5: Hoàn tất, Đóng gói Git Commit & Dọn Dẹp Subagent
Khi `review-report.md` đạt `APPROVED`:
1. **Kiểm tra trạng thái Git & Cập nhật Manifest Gốc**:
   - Nếu trong các phase trước có cờ `[DEPENDENCY REQUIRED]`, Tech Lead Orchestrator trực tiếp kiểm tra và cập nhật `pyproject.toml` hoặc `src/frontend/package.json`.
   - Chạy `git status --short` kiểm tra toàn bộ file mới và thay đổi trong `src/`, `docs/specs/<feature-slug>/`, và các file manifest.
2. **Thực hiện Commit chuẩn hóa**:
   ```bash
   git add src/ docs/specs/<feature-slug>/
   git add pyproject.toml src/frontend/package*.json 2>/dev/null || true
   git commit -m "feat(<feature-slug>): implement <tên tính năng ngắn gọn>

   - DB: add SQLAlchemy 2.0 models & migrations in src/db/
   - Backend: implement FastAPI schemas, services & endpoints in src/backend/
   - Frontend: build Next.js UI components & typed API client in src/frontend/
   - Quality: 100% tests passed, code review approved
   - Specs: docs/specs/<feature-slug>/plan.md"
   ```
3. **Tự Động Hóa Dọn Dẹp Subagent (Subagent Lifecycle Cleanup)**:
   - Sau khi commit hoàn tất, Tech Lead Orchestrator **tự động gọi công cụ `manage_subagents` với `Action: "kill"`** cho toàn bộ Conversation IDs trong `SQUAD_REGISTRY` (hoặc `Action: "kill_all"`).
   - *Mục đích*: Giải phóng tài nguyên hệ thống, bộ nhớ và các background tasks của Antigravity 2.0, bảo đảm không bị rò rỉ context hoặc subagents zombie cho tính năng tiếp theo.
4. Tổng hợp báo cáo nghiệm thu hoàn tất cho User kèm xác nhận dọn dẹp sạch sẽ.
