# 🌟 DỰ ÁN MẪU THAM KHẢO (GOLDEN REFERENCE PROJECT): MOTOCARE

> Đây là thành phẩm mẫu hoàn chỉnh được sinh tự động bởi hệ thống **Multi-Agents SDLC (Antigravity 2.0)** qua 4 giai đoạn khép kín.
> Dự án được lưu trữ tại đây nhằm mục đích tham khảo kiến trúc (Golden Reference), không làm ảnh hưởng đến không gian làm việc sạch `workspaces/` của Template.

---

## 📊 KẾT QUẢ NGHIỆM THU ĐẠT ĐƯỢC
- **Backend Clean Architecture:** Python 3.12 + FastAPI v0.110+, phân tầng triệt để (`core` -> `models` -> `schemas` -> `repositories` -> `services` -> `routers`).
- **ORM & Migrations:** SQLAlchemy 2.0 Declarative Mapped Models + Alembic 1.13+ (**Zero Schema Drift** qua `alembic check`).
- **Code Coverage (pytest-cov):** Đạt **90%** độ phủ kiểm thử tự động trên toàn bộ API Routers và Services.
- **Frontend:** React Native (TypeScript) đa màn hình (`AuthScreen`, `CatalogScreen`, `BookingScreen`, `TrackingScreen`), REST API Client, Zustand Store và Jest Unit Test Suite (`run_tests.cjs`) + E2E Contracts (`run_e2e_tests.cjs`).
- **DevOps:** Multi-stage Dockerfile và Docker Compose (FastAPI :8000 + PostgreSQL 15 :5432).

---

## 📂 CẤU TRÚC THÀNH PHẨM TRONG THƯ MỤC NÀY
```text
examples/motocare_reference/
├── output_project/             # Toàn bộ mã nguồn hoàn chỉnh (backend, frontend, infra)
├── artifacts/                  # Toàn bộ tài liệu SDLC sinh ra (PRD, OpenAPI, ERD, Security, Review Gates)
└── checkpoints/                # Lịch sử Checkpoint trạng thái máy SDLC State Machine
```
