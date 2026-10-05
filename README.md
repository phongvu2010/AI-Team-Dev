# AI Team Dev — Hệ thống Multi-Agent trên Antigravity 2.0

Workspace này đã được cấu hình chuẩn **Native Antigravity 2.0 Multi-Agent** theo **Mô hình Ma trận (Matrix Architecture)** kết hợp quy trình **2-Wave Execution**, giải quyết triệt để 4 trụ cột kỹ thuật:

1. 🔄 **Cơ Chế Phản Hồi Tự Động (Feedback Loop & Circuit Breaker)**: Vòng lặp sửa lỗi 2 chiều cho cả Testing và Code Review với giới hạn 3 lần lặp và cơ chế ngắt mạch an toàn.
2. 📐 **Đồng Bộ Hợp Đồng Dữ Liệu & API (Data & API Contract Synchronization)**: Loại bỏ rủi ro lệch chuẩn qua Ma trận ánh xạ 3 tầng (Database $\leftrightarrow$ Backend $\leftrightarrow$ Frontend) và chuẩn hóa casing `snake_case`.
3. 🛡️ **Rào Chắn An Toàn Dòng Lệnh (CLI Execution Guardrails)**: Phân quyền thực thi lệnh theo vai trò (Role-based Whitelist/Blacklist) và bảo vệ phân vùng file nghiêm ngặt.
4. 📋 **Tiêu Chuẩn Hóa Hồ Sơ Bàn Giao (Artifact Handover Schema)**: Chuẩn hóa toàn diện định dạng Metadata Header và phiếu báo lỗi/thẩm định có cấu trúc tại `docs/specs/<feature-slug>/`.

> 🚀 **Cẩm Nang Sử Dụng Chi Tiết**:
> - Xem [TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md) để biết cách khởi tạo repo mới và cài đặt môi trường Day-0.
> - Xem [WORKFLOW.md](WORKFLOW.md) để nắm toàn bộ Quy trình Vận hành Chuẩn (SOP) 7 giai đoạn từ ý tưởng đến bàn giao.

---

## 🎯 Định Vị Template: Dự Án Nào Phù Hợp Chính Xác?

Template này được tối ưu hoá chuyên sâu cho các dự án **Full-Stack Web Applications Hiện Đại** sử dụng bộ đôi công nghệ **Python (FastAPI) + TypeScript (Next.js)** kết hợp cơ sở dữ liệu quan hệ **PostgreSQL**.

### 1. Hệ sinh thái Công nghệ Cố định (Fixed Stack Foundation)
- **Database (`src/db/`)**: PostgreSQL 16+, SQLAlchemy 2.0 (Async), asyncpg, Alembic migrations tự động. Tương thích cross-DB tuyệt đối giữa SQLite in-memory test và PostgreSQL runtime (UUID sinh qua Python `default=uuid.uuid4`, mảng dữ liệu qua `JSON`), tích hợp sẵn Seed Runner tại `src/db/seeds/`.
- **Backend API (`src/backend/`)**: Python 3.11+, FastAPI (REST API), Pydantic v2 validation, Ruff linter, Pytest.
- **Frontend Web (`src/frontend/`)**: React 19, Next.js (App Router), TypeScript (Strict), Tailwind CSS.
- **Kiểm thử Cô lập**: SQLite async in-memory fallback giúp chạy toàn bộ test không cần cài PostgreSQL local.

### 2. Các Loại Dự Án Phù Hợp Nhất (Sweet Spot / Best Fit)
| Loại hình dự án | Mô tả chi tiết | Độ phù hợp |
| :--- | :--- | :---: |
| **SaaS Web Platforms** | Các ứng dụng SaaS quản lý thuê bao, xác thực, phân quyền (RBAC), thanh toán và dashboard báo cáo số liệu. | ⭐⭐⭐⭐⭐ (Hoàn hảo) |
| **B2B / B2C Web Portals** | Cổng thông tin khách hàng, cổng đối tác, sàn dịch vụ, booking, marketplace vừa và nhỏ. | ⭐⭐⭐⭐⭐ (Hoàn hảo) |
| **Internal Tools & Dashboards** | Hệ thống CRM nội bộ, quản trị bán hàng, theo dõi đơn hàng, quản lý kho bãi, nhân sự. | ⭐⭐⭐⭐⭐ (Hoàn hảo) |
| **Startup MVP $\to$ Production** | Dự án khởi nghiệp cần đưa tính năng ra thị trường thần tốc bằng AI nhưng kiến trúc vẫn sạch và mở rộng được. | ⭐⭐⭐⭐⭐ (Hoàn hảo) |
| **REST API Micro/Modular Backend** | Cần một Backend API chuẩn mực, có Swagger UI tự động và tài liệu hợp đồng API chặt chẽ. | ⭐⭐⭐⭐ (Rất tốt) |

### 3. Khi Nào KHÔNG NÊN Dùng Template Này? (Non-Goals)
- ❌ **Dự án Mobile App thuần (Native iOS/Android / Flutter / React Native)**: Template này chỉ xây dựng Web App Next.js (trừ khi bạn chỉ cần phần Backend API).
- ❌ **Hệ thống Microservices đa ngôn ngữ (Java, Go, Rust, .NET)**: Template này thiết kế tối ưu cho mô hình **Modular Monolith** hoặc 2-Tier (FastAPI + Next.js).
- ❌ **Data Science / Machine Learning thuần túy**: Nếu dự án chỉ chạy Jupyter Notebook, huấn luyện model PyTorch/TensorFlow lớn mà không cần web/API.
- ❌ **Website tĩnh đơn giản (Static Blog, Landing Page 1 trang)**: Nên dùng Astro, Hugo hoặc Next.js static thuần không cần DB/FastAPI.

---

## 🏗️ Sơ Đồ Quy Trình Thực Thi 6 Pha (Multi-Agent Pipeline)

```text
                                  ┌────────────────────────┐
                                  │      0. BA AGENT       │
                                  │ (docs/specs/<slug>/)   │
                                  │  - User Interview (ask)│
                                  │  - PRD / Business Spec │
                                  │  - User Sign-off Gate  │
                                  └───────────┬────────────┘
                                              │
                                              ▼
                                  ┌────────────────────────┐
                                  │      1. PLANNER        │
                                  │ (docs/specs/<slug>/)   │
                                  │  - Ingest prd.md       │
                                  │  - Cross-Layer Matrix  │
                                  │  - REST API Contract   │
                                  └───────────┬────────────┘
                                              │
                                              ▼
                ┌─────────────────────────────────────────────────────────────┐
                │              2. DEV SQUADS (2-Wave Execution)               │
                │                                                             │
                │  [Wave 1 - Song song]                                       │
                │  ├── db-dev       ──► src/db/ (SQLAlchemy 2.0 Models)       │
                │  └── frontend-dev ──► src/frontend/ (Next.js UI & Types)    │
                │                                                             │
                │  [Wave 2]                                                   │
                │  └── backend-dev  ──► src/backend/ (FastAPI + Pydantic v2)  │
                └──────────────────────────────┬──────────────────────────────┘
                                              │
                                              ▼
                                  ┌────────────────────────┐
                                  │      3. QA TESTER      │
                                  │  (pytest / vitest/tsc) │
                                  │  - Test Metrics        │
                                  │  - Structured Bug List │
                                  └───────────┬────────────┘
                                              │ ◄── [Self-Healing Loop: Max 3x]
                                              ▼
                                  ┌────────────────────────┐
                                  │    4. CODE REVIEWER    │
                                  │ (Token-optimized diff) │
                                  │  - Quality Scorecard   │
                                  │  - Structured Findings │
                                  └───────────┬────────────┘
                                              │ ◄── [Review-Fix Loop: Max 3x]
                                              ▼
                                  ┌────────────────────────┐
                                  │   5. COMMIT & HANDOFF  │
                                  │ (Conventional Commits) │
                                  └────────────────────────┘
```

---

## 👥 Danh Sách 7 Subagents Chuyên Biệt & Rào Chắn Lệnh

| Subagent ID | Vai trò (Role) | Thư mục quyền sở hữu | Lệnh được phép (Whitelist) | Nhiệm vụ chính |
| :--- | :--- | :--- | :--- | :--- |
| [`ba`](.agents/agents/ba.md) | Business Analyst & Requirements Engineer | `docs/specs/<slug>/` | Phỏng vấn (`ask_question`), chỉ đọc/ghi file (`view_file`, `write_to_file`, `replace_file_content`) | Phỏng vấn làm rõ yêu cầu, xuất bản `prd.md` (FRs, Business Rules, Edge Cases, BACs) |
| [`planner`](.agents/agents/planner.md) | System Architect & Planner | `docs/specs/<slug>/` | Chỉ đọc/ghi file (`view_file`, `write_to_file`) | Xuất bản `plan.md` (Cross-Layer Data Contract Matrix, REST API Spec, UI Spec, AC Matrix) |
| [`db-dev`](.agents/agents/db-dev.md) | Database Specialist | `src/db/` | `.venv/bin/ruff check src/db/`, `python3 -m py_compile`, `alembic`, `runner.py` | Tạo SQLAlchemy 2.0 models, migrations, repositories async, seeds |
| [`frontend-dev`](.agents/agents/frontend-dev.md) | Frontend Specialist | `src/frontend/` | `npm --prefix src/frontend run typecheck`, `run lint`, `run build` | Tạo Next.js pages/components, TypeScript interfaces (`snake_case`), mock fixtures, 4 UI states |
| [`backend-dev`](.agents/agents/backend-dev.md) | Backend Specialist | `src/backend/` | `.venv/bin/ruff check src/backend/`, `python3 -m py_compile` | Tạo Pydantic v2 schemas (`snake_case`), async services, FastAPI endpoints kết nối `src/db/` |
| [`qa-tester`](.agents/agents/qa-tester.md) | QA & Automated Tester | `docs/specs/<slug>/`, `tests/` | `.venv/bin/ruff check src/`, `PYTHONPATH=src .venv/bin/pytest`, `run typecheck` | Chạy linter, automated tests (SQLite fallback), xuất `test-report.md` kèm Structured Bug Tickets |
| [`code-reviewer`](.agents/agents/code-reviewer.md) | Principal Code Reviewer | `docs/specs/<slug>/` | `git status --short`, `git diff --stat`, `git diff` | Audit `git diff`, kiểm tra N+1 query, bảo mật OWASP, xuất `review-report.md` |

---

## 📁 Cấu Trúc Thư Mục Workspace

```text
AI Team Dev/
├── AGENTS.md                                      # Quy tắc điều phối Tech Lead / Orchestrator toàn cục
├── WORKFLOW.md                                    # Cẩm nang SOP 7 giai đoạn & bộ mẫu thông điệp Dispatch
├── TEMPLATE_GUIDE.md                              # Hướng dẫn chi tiết sử dụng template cho dự án mới
├── README.md                                      # Tổng quan dự án, kiến trúc & danh sách tác tử
├── pyproject.toml                                 # Khởi tạo dependencies & pytest pythonpath=["src"]
├── docker-compose.yml                             # Khởi chạy Full-Stack: PostgreSQL 16, FastAPI Backend & Next.js 15
├── .dockerignore                                  # Tối ưu hóa build context Docker
├── .env.example                                   # Biến môi trường mẫu cho DB, API, Frontend
├── .gitignore                                     # Bỏ qua bytecode, node_modules, cache
├── .agents/
│   ├── agents/                                    # Định nghĩa 6 Subagents chuyên biệt kèm Guardrails
│   │   ├── planner.md
│   │   ├── db-dev.md
│   │   ├── backend-dev.md
│   │   ├── frontend-dev.md
│   │   ├── qa-tester.md
│   │   └── code-reviewer.md
│   └── skills/                                    # Bộ Skills & Runbooks tải theo ngữ cảnh
│       ├── team-pipeline/
│       │   ├── SKILL.md
│       │   └── resources/                         # Bộ mẫu hồ sơ bàn giao chuẩn hóa
│       │       ├── plan-template.md               # Template kế hoạch & Data Contract Matrix
│       │       ├── test-report-template.md        # Template báo cáo QA & Structured Bug Tickets
│       │       └── review-report-template.md      # Template thẩm định & Quality Scorecard
│       ├── db-sqlalchemy-alembic/SKILL.md
│       ├── backend-fastapi/SKILL.md
│       └── frontend-nextjs/SKILL.md
├── src/                                           # Thư mục mã nguồn thực thi tập trung
│   ├── db/                                        # Models, session, repositories, migrations, seeds
│   │   └── AGENTS.md                              # Luật cục bộ tầng Database
│   ├── backend/                                   # FastAPI app, schemas, services, api routers, tests
│   │   ├── Dockerfile                             # Production Dockerfile cho FastAPI backend (non-root)
│   │   └── AGENTS.md                              # Luật cục bộ tầng Backend
│   └── frontend/                                  # Next.js app router, components, lib api, types
│       ├── Dockerfile                             # Multi-stage standalone Dockerfile (~110MB)
│       ├── .dockerignore                          # Bỏ qua node_modules, .next khi build frontend
│       └── AGENTS.md                              # Luật cục bộ tầng Frontend
└── docs/
    └── specs/                                     # Hồ sơ bàn giao tính năng chuẩn hóa
        └── README.md
```

---

## 🚀 Cách Sử Dụng Trên Giao Diện Antigravity 2.0

### Cách 1: Chạy Toàn Bộ Quy Trình Tự Động (Full-Flow)
Người dùng chỉ cần nhập yêu cầu tính năng vào chat Antigravity, ví dụ:
> *"Hãy triển khai tính năng Quản lý Danh mục (Category Management) gồm bảng categories (id, name, slug, description), CRUD API trên FastAPI và trang giao diện trên Next.js theo quy trình Multi-Agent."*

Agent chính (**Tech Lead Orchestrator**) sẽ tự động:
1. Gọi `planner` lập bản thiết kế tại `docs/specs/category-management/plan.md` (kèm Cross-Layer Data Contract Matrix).
2. **Wave 1**: Gọi song song `db-dev` (viết model trong `src/db/`) và `frontend-dev` (dựng UI/Types trong `src/frontend/`).
3. **Wave 2**: Gọi `backend-dev` viết router & service trong `src/backend/` kết nối trực tiếp `src/db/`.
4. Gọi `qa-tester` chạy kiểm tra `ruff` linter và bộ kiểm thử tự động với `PYTHONPATH=src .venv/bin/pytest src/backend/tests -v` và xuất `test-report.md`. (Nếu lỗi, tự kích hoạt vòng lặp Self-Healing).
5. Gọi `code-reviewer` audit qua `git diff` và xuất `review-report.md` (`APPROVED`). (Nếu lỗi, tự kích hoạt vòng lặp Review-Fix).
6. **Đóng gói & Commit**: Tự động rà soát `git status` và tạo commit chuẩn Conventional Commits `feat(<slug>): ...` ghi nhận mốc hoàn thành.

### Cách 2: Gọi Trực Tiếp Từng Squad Hoặc Giai Đoạn (Direct Squad Invocation)
- *"Nhờ `planner` thiết kế kiến trúc phân hệ Sản phẩm."*
- *"Nhờ `db-dev` thêm trường `thumbnail_url` vào bảng `categories` tại `src/db/`."*
- *"Nhờ `backend-dev` viết thêm endpoint lọc danh mục tại `src/backend/`."*
- *"Nhờ `frontend-dev` hoàn thiện component CategoryCard tại `src/frontend/`."*
- *"Nhờ `qa-tester` kiểm tra lint và chạy lại pytest cho tầng backend."*
- *"Nhờ `code-reviewer` review các thay đổi mới nhất qua git diff."*
