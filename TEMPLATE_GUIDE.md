# Hướng dẫn Sử dụng Template Multi-Agent Cho Dự Án Mới

Tài liệu này hướng dẫn cách sử dụng repository này làm **Template Chuẩn (Starter Template)** để khởi tạo và phát triển các dự án phần mềm mới cùng **Hệ thống AI Team Dev (Antigravity 2.0)**.

Template đã được thiết kế và kiểm thử chuyên sâu nhằm giải quyết triệt để 4 thách thức cốt lõi trong phát triển phần mềm đa tác tử (Multi-Agent):
1. **Cơ chế Phản hồi Tự động (Feedback Loop & Circuit Breaker)**: Vòng lặp sửa lỗi 2 chiều cho cả Testing và Code Review có quản lý trạng thái, giới hạn tối đa 3 lần lặp và cơ chế ngắt mạch an toàn.
2. **Đồng bộ Hợp đồng Dữ liệu & API (Data & API Contract Synchronization)**: Loại bỏ rủi ro desync thông qua Ma trận ánh xạ dữ liệu 3 tầng (Database $\leftrightarrow$ Backend $\leftrightarrow$ Frontend) và chuẩn hóa casing `snake_case`.
3. **Rào chắn An toàn Thực thi Lệnh (CLI Execution Guardrails)**: Phân quyền thực thi lệnh theo vai trò (Role-based Whitelist & Blacklist) và bảo vệ nghiêm ngặt phân vùng file.
4. **Tiêu chuẩn hóa Hồ sơ Bàn giao (Artifact Handover Schema)**: Chuẩn hóa toàn diện định dạng Metadata Header và phiếu báo lỗi/thẩm định có cấu trúc tại `docs/specs/<feature-slug>/`.

---

## 1. Tổng quan Kiến trúc Template

Template này được thiết kế theo **Mô hình Ma trận (Matrix Architecture)** kết hợp quy trình **2-Wave Execution**, phân tách quyền sở hữu thư mục nghiêm ngặt:

```text
[User Request]
      │
      ▼
┌───────────────────────────────────────────────────────────┐
│               TECH LEAD / ORCHESTRATOR (Main)             │
└───────────────────────────────────────────────────────────┘
      │
      ├──► Phase 1: PLANNER (`planner`)
      │      └── docs/specs/<feature-slug>/plan.md
      │          (Metadata + Cross-Layer Matrix + REST API Contract + UI Spec + AC Matrix)
      │
      ├──► Phase 2: DEV SQUADS (2-Wave Pipelined Execution)
      │      ├── Wave 1 (Song song):
      │      │     ├── `db-dev`       ──► src/db/ (SQLAlchemy 2.0 + Alembic)
      │      │     └── `frontend-dev` ──► src/frontend/ (Next.js + Strict TS + Mocks)
      │      ├── [Wave Handshake Gate] (Kích hoạt ngay khi DB xong models)
      │      └── Wave 2 (Pipelined):
      │            └── `backend-dev`  ──► src/backend/ (FastAPI + Pydantic v2, gối đầu song song)
      │
      ├──► Phase 3: TESTING & FEEDBACK LOOP (`qa-tester`)
      │      ├── Linter + Pytest SQLite in-memory + Frontend Typecheck
      │      └── docs/specs/<feature-slug>/test-report.md
      │          └── [SELF-HEALING ACTION REQUIRED] -> [FIX-COMPLETED] (Max 3 retries)
      │
      ├──► Phase 4: CODE REVIEW & AUDIT (`code-reviewer`)
      │      ├── Token-optimized audit qua git diff
      │      └── docs/specs/<feature-slug>/review-report.md
      │          └── [REVIEW-FIX ACTION REQUIRED] -> [FIX-COMPLETED] (Max 3 retries)
      │
      └──► Phase 5: PACKAGING, COMMIT & CLEANUP (Tech Lead Orchestrator)
             ├── Conventional Commits: feat(<feature-slug>): ...
             └── Subagent Cleanup: manage_subagents(Action="kill")
```

---

## 2. Tiêu Chí Lựa Chọn: Dự Án Nào Nên Sử Dụng Template Này?

Nếu bạn là người mới sử dụng template này, hãy dùng bảng tiêu chí dưới đây để xác định dự án của bạn có phải là ứng viên hoàn hảo hay không:

### 2.1. Checklist Đánh giá Phù hợp Dự án (Quick Decision Matrix)
Trả lời các câu hỏi sau cho dự án bạn dự định xây dựng:
1. **Bạn có cần một ứng dụng Web tương tác hiện đại không?** (Next.js 15, React 19, Tailwind CSS) $\to$ **CÓ**
2. **Bạn có cần một Backend API bất đồng bộ hiệu năng cao bằng Python không?** (FastAPI, Pydantic v2) $\to$ **CÓ**
3. **Bạn có lưu trữ dữ liệu quan hệ có ràng buộc, giao dịch ACID không?** (PostgreSQL, SQLAlchemy 2.0) $\to$ **CÓ**
4. **Bạn có muốn AI tự động thiết kế, lập trình, kiểm thử và review code độc lập không?** (Antigravity 2.0 Multi-Agent) $\to$ **CÓ**

> 👉 **Nếu có từ 3 câu trả lời "CÓ" trở lên**: Đây chính xác là template dành riêng cho dự án của bạn!

### 2.2. Các Trường Hợp Sử Dụng Điển Hình (Sweet Spot)
* **Dự án SaaS Khởi nghiệp (Startup SaaS MVP $\to$ Production)**: Các dịch vụ phần mềm dạng thuê bao cần xác thực người dùng, dashboard báo cáo, quản lý thanh toán và phân quyền (RBAC).
* **Cổng thông tin & Nền tảng Quản trị (Internal Tools & Dashboards)**: CRM nội bộ, ERP mini, hệ thống quản trị kho, quản lý đặt lịch hẹn/booking, quản lý nhân sự hoặc đơn hàng.
* **Sản phẩm Web B2B / B2C**: Sàn giao dịch dịch vụ, cổng tiếp nhận yêu cầu khách hàng, website thương mại điện tử vừa và nhỏ.
* **Hệ thống REST API Chuyên nghiệp**: Cần backend API chuẩn mực, tài liệu Swagger tự động kèm bộ kiểm thử tự động cô lập.

### 2.3. Các Trường Hợp KHÔNG Phù Hợp (Non-Goals)
* ❌ Ứng dụng di động thuần (iOS/Android native hoặc Flutter/React Native) — trừ trường hợp bạn chỉ dùng phần `src/backend/` và `src/db/` làm REST API cho mobile app.
* ❌ Hệ sinh thái Microservices đa ngôn ngữ phân tán (Java Spring, Go, Rust, .NET kết hợp).
* ❌ Các tác vụ Khoa học Dữ liệu / AI Training thuần túy (chỉ chạy Notebook phân tích dữ liệu, không có Web UI).
* ❌ Website tĩnh đơn giản không cần cơ sở dữ liệu (Static Blog, Landing Page một trang).

---

## 3. Bước 1: Khởi tạo Repository Mới

### Cách A: Sử dụng tính năng GitHub Template (Khuyên dùng)
1. Trên repository này tại GitHub, bấm nút **"Use this template"** $\to$ chọn **"Create a new repository"**.
2. Đặt tên repository cho dự án mới của bạn (ví dụ: `my-saas-platform`, `ecommerce-core`).
3. Clone repository mới về máy:
   ```bash
   git clone <URL_REPO_MOI>
   cd <THU_MUC_REPO_MOI>
   ```

### Cách B: Sao chép thủ công (Local Copy)
Nếu khởi tạo offline hoặc dùng Git Server nội bộ:
```bash
# Clone hoặc copy template sang thư mục mới
cp -r "AI Team Dev" "my-new-project"
cd "my-new-project"

# Khởi tạo lại lịch sử Git cho dự án mới
rm -rf .git
git init
git add .
git commit -m "chore: initial commit from ai-team-dev template"
```

---

## 4. Bước 2: Thiết lập Môi trường Phát triển (Chỉ mất 2 phút)

Dự án sử dụng Python 3.11+ cho Backend/DB và Node.js 18+ cho Frontend Next.js.

### 2.1. Cấu hình biến môi trường
Tạo file `.env` từ file mẫu `.env.example`:
```bash
cp .env.example .env
```

### 2.2. Thiết lập Python Virtualenv (Backend & Database)
```bash
# 1. Tạo virtualenv .venv
python3 -m venv .venv

# 2. Kích hoạt môi trường
source .venv/bin/activate    # Trên macOS / Linux
# hoặc: .venv\Scripts\activate trên Windows

# 3. Nâng cấp pip và cài đặt dependencies ở chế độ editable
pip install --upgrade pip
pip install -e ".[dev]"
```

### 2.3. Cài đặt dependencies Frontend (Next.js)
```bash
npm --prefix src/frontend install
```

### 2.4. Khởi chạy Ứng dụng Bằng Docker (Tuỳ chọn)

Hệ thống cung cấp sẵn 2 chế độ Docker linh hoạt:

* **Chế độ 1 — Chạy Full-Stack 1-Click (Khuyên dùng khi demo, review hoặc staging)**:
  Khởi chạy trọn vẹn cả 3 tầng (PostgreSQL 16, FastAPI Backend và Next.js 15 Frontend) trong cùng mạng nội bộ:
  ```bash
  docker compose up --build -d
  ```
  - Frontend Web UI: `http://localhost:3000`
  - FastAPI Swagger Docs: `http://localhost:8000/docs`
  - Backend Health Check: `http://localhost:8000/health`
  - PostgreSQL Port: `localhost:5432`

* **Chế độ 2 — Chỉ chạy PostgreSQL Container (Dành cho Dev lập trình trên máy host)**:
  Khi bạn muốn dev trực tiếp qua Python virtualenv và npm trên máy host:
  ```bash
  docker compose up -d postgres
  ```
  *(Lưu ý: Bộ test tự động mặc định sử dụng SQLite async in-memory, do đó bạn không nhất thiết phải bật Docker PostgreSQL chỉ để chạy test).*

### 2.5. Nạp Dữ liệu Mẫu Khởi đầu (Seed Data — Tuỳ chọn)
Khi đã khởi chạy PostgreSQL hoặc cần nạp dữ liệu mẫu ban đầu:
```bash
PYTHONPATH=src .venv/bin/python src/db/seeds/runner.py
```

---

## 5. Bước 3: Kiểm chứng Môi trường Day-0 (Smoke Verification)

Trước khi bắt đầu bất kỳ câu lệnh AI nào, hãy chạy lệnh kiểm tra toàn diện để đảm bảo chuỗi công cụ đã sẵn sàng:

```bash
.venv/bin/ruff check src/ && PYTHONPATH=src .venv/bin/pytest src/backend/tests -v && npm --prefix src/frontend run build
```

**Kết quả kỳ vọng**:
* **Ruff**: `All checks passed!`
* **Pytest**: `3 passed in 0.03s` (Pass cả endpoint `/health` và session async DB)
* **Frontend Build**: `✓ Compiled successfully` (Next.js App Router render static pages, typecheck sạch sẽ).

---

## 6. Bước 4: Bắt đầu Phát triển Tính năng cùng AI Team

Mở thư mục dự án mới trong **Antigravity 2.0**, bạn đóng vai trò là **Product Owner / User**, giao tiếp trực tiếp với **Tech Lead Orchestrator**:

### Mẫu câu lệnh (Prompt Template) để chạy toàn bộ quy trình:
> *"Hãy phát triển tính năng **[Tên tính năng]** (slug: `[feature-slug]`) theo quy trình Multi-Agent Dev Team:*
> - *Yêu cầu nghiệp vụ: [Mô tả chi tiết các màn hình, chức năng, user flow]*
> - *Cơ sở dữ liệu: [Các bảng dữ liệu cần tạo, trường chính, quan hệ]*
> - *API: [Các endpoints CRUD hoặc nghiệp vụ cần cung cấp]*
> - *Frontend: [Trang giao diện Next.js, component, trạng thái UX]*"

### Ví dụ Thực tế:
> *"Hãy phát triển tính năng Quản lý Sản phẩm (slug: `product-catalog`) theo quy trình Multi-Agent Dev Team:*
> - *Database: Tạo bảng `products` (id, title, sku, price, stock, is_active, created_at, updated_at).*
> - *API: Cung cấp CRUD REST API đầy đủ trên FastAPI với phân trang `page`, `size`.*
> - *Frontend: Xây dựng trang danh sách sản phẩm Next.js có thanh tìm kiếm, bảng dữ liệu responsive và nút tạo sản phẩm mới."*

---

## 7. Các Chế độ Thực thi Linh hoạt

Tùy vào nhu cầu công việc, bạn có thể chọn 1 trong 2 chế độ:

### Chế độ 1: Chạy Full-Flow (Tự động 5 Phase)
Tech Lead sẽ tự động điều phối:
1. `planner` $\to$ tạo `docs/specs/<feature-slug>/plan.md` (kèm Cross-Layer Data Contract Matrix).
2. Wave 1: Gọi song song `db-dev` (`src/db/`) & `frontend-dev` (`src/frontend/`).
3. Wave 2 (Pipelined): Ngay khi `db-dev` hoàn thành models sạch sẽ qua Handshake Gate, kích hoạt ngay `backend-dev` (`src/backend/`) chạy gối đầu song song với `frontend-dev` mà không cần chờ FE xong 100%.
4. `qa-tester` $\to$ chạy ruff, pytest, typecheck $\to$ tạo `docs/specs/<feature-slug>/test-report.md`. Tự động kích hoạt Vòng lặp Self-Healing nếu có lỗi.
5. `code-reviewer` $\to$ audit `git diff` $\to$ tạo `docs/specs/<feature-slug>/review-report.md`. Tự động kích hoạt Review-Fix loop nếu có lỗi.
6. Tự động đóng gói commit & dọn dẹp subagents: `git commit` $\to$ `manage_subagents` (`Action: "kill"`) toàn bộ squads trong `SQUAD_REGISTRY`.

### Chế độ 2: Gọi Trực tiếp Từng Tác tử Chuyên biệt (Direct Squad Invocation)
- **Cần bản thiết kế**: *"Nhờ `planner` thiết kế kiến trúc phân hệ Đơn hàng."*
- **Sửa Database**: *"Nhờ `db-dev` thêm index cho cột `sku` bảng `products` và tạo migration Alembic."*
- **Viết thêm API**: *"Nhờ `backend-dev` thêm endpoint lọc sản phẩm theo khoảng giá."*
- **Làm UI**: *"Nhờ `frontend-dev` làm component ProductFilterBar xử lý đủ 4 trạng thái."*
- **Chạy kiểm thử**: *"Nhờ `qa-tester` kiểm tra lint và chạy test suite."*
- **Audit bảo mật/code**: *"Nhờ `code-reviewer` review các thay đổi mới qua git diff."*

---

## 8. Các Nguyên tắc Sống còn Cần Nhớ (Best Practices & Guardrails)

1. **Tuyệt đối không xoá thư mục `src/`**:
   - `src/` chứa các điểm neo (Anchor Points) và các file luật cục bộ [src/db/AGENTS.md](src/db/AGENTS.md), [src/backend/AGENTS.md](src/backend/AGENTS.md), [src/frontend/AGENTS.md](src/frontend/AGENTS.md).
2. **Tuân thủ Tuyệt đối Rào Chắn Lệnh & Bảo vệ File Cấu hình Gốc (CLI Guardrails)**:
   - Các tác tử chỉ chạy lệnh trong danh mục Whitelist phân quyền.
   - Subagents tuyệt đối không tự ý sửa đổi file cấu hình gốc (`pyproject.toml`, `docker-compose.yml`, `alembic.ini`, `src/frontend/package.json`). Khi cần thêm thư viện mới, subagent BẮT BUỘC chỉ cắm cờ `[DEPENDENCY REQUIRED]`. Độc quyền Tech Lead Orchestrator chỉnh sửa các file manifest này để tránh race condition trong `Workspace: "inherit"`.
   - Tuyệt đối cấm chạy lệnh cài đặt trần `pip/npm install` trong sandbox.
   - Luôn sử dụng `.venv/bin/pytest` và `.venv/bin/ruff` thay vì gọi lệnh trần.
3. **Phân vùng File Tuyệt đối (File Isolation)**:
   - `db-dev` chỉ ghi `src/db/`.
   - `backend-dev` chỉ ghi `src/backend/`.
   - `frontend-dev` chỉ ghi `src/frontend/`.
   - `qa-tester` & `code-reviewer` không sửa code nghiệp vụ mà báo cáo lại để Dev Squad sửa chữa thông qua vòng lặp phản hồi tự động.
4. **Đồng bộ Hợp đồng Dữ liệu (Contract Synchronization)**:
   - Toàn bộ payload REST API quy định **thống nhất sử dụng `snake_case`**.
   - Mọi thuộc tính phải ánh xạ 1:1 theo Ma trận dữ liệu 3 tầng trong `plan.md`. Không dùng `any` trong TypeScript.
5. **Cơ chế Vòng Lặp Phản Hồi & Ngắt Mạch (Circuit Breaker)**:
   - Mọi phản hồi sửa lỗi tuân thủ giao thức `[SELF-HEALING ACTION REQUIRED]` / `[REVIEW-FIX ACTION REQUIRED]` và `[FIX-COMPLETED]`.
   - Tối đa 3 vòng lặp cho mỗi tính năng. Nếu vượt quá, hệ thống tự động ngắt mạch và báo cáo cho con người xử lý.
6. **Cross-DB Type Safety (UUID & ARRAY)**:
   - UUID khóa chính luôn dùng `from sqlalchemy import Uuid` kèm `default=uuid.uuid4` ở Python (hoặc kế thừa `UUIDPrimaryKeyMixin` từ `src/db/base.py`). Không dùng `server_default=text("gen_random_uuid()")`.
   - Danh sách mảng dùng `from sqlalchemy import JSON` (`default=list`) hoặc variant thay vì `ARRAY` trần để SQLite test không bị fail `CompileError`.
7. **Đồng bộ Mock → Live API**:
   - Trong Wave 1, Frontend sử dụng mock data thông qua `isMockMode()` (`NEXT_PUBLIC_USE_MOCKS=true`).
   - Khi hoàn thành Wave 2, bắt buộc chuyển `NEXT_PUBLIC_USE_MOCKS=false` để kết nối trực tiếp với FastAPI backend live.
8. **Chiến lược Không gian làm việc (`Workspace: "inherit"`)**:
   - Khi gọi `invoke_subagent` cho các Dev Squads, chỉ định `"Workspace": "inherit"` vì ranh giới thư mục hoàn toàn độc lập (`src/db/` vs `src/frontend/`), giúp Wave 2 và QA nhìn thấy code mới ngay lập tức mà không cần merge branch.
9. **Khởi tạo Migration Offline**:
   - Khi không có PostgreSQL container, chạy `PYTHONPATH=src .venv/bin/python src/db/migrations/generate_offline_migration.py <slug>` để tự động tạo file migration chuẩn có revision ID hợp lệ.
10. **Tối ưu Token cho Code Review**:
    - Dùng lệnh lọc `git diff -- src/ docs/ ':!*package-lock.json' ':!*.lock'` để loại bỏ lockfiles, dồn 100% token budget vào thẩm định kiến trúc, N+1 query và bảo mật.
