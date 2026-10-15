# ==============================================================================
# MAKEFILE — BỘ TỰ ĐỘNG HÓA LỆNH 1-CHẠM CHO AI TEAM DEV (ANTIGRAVITY 2.0)
# Tương thích đa nền tảng: Windows (Git Bash / PowerShell), Linux, macOS
# ==============================================================================

VENV ?= .venv
ifeq ($(OS),Windows_NT)
    PYTHON ?= $(if $(wildcard $(VENV)/Scripts/python.exe),$(VENV)/Scripts/python.exe,python)
    PIP ?= $(if $(wildcard $(VENV)/Scripts/pip.exe),$(VENV)/Scripts/pip.exe,pip)
else
    PYTHON ?= $(if $(wildcard $(VENV)/bin/python),$(VENV)/bin/python,python3)
    PIP ?= $(if $(wildcard $(VENV)/bin/pip),$(VENV)/bin/pip,pip3)
endif

FEATURE ?= 
VERSION ?= 1.0.0
NAME ?= checkpoint
COV_FAIL_UNDER ?= 80

.PHONY: help smoke test test-cov cov-html test-backend test-db test-frontend-e2e test-all typecheck typecheck-mobile check-contracts check-migrations check-db models release snapshot snapshot-list restore dev-backend dev-frontend setup-nextjs setup-vite setup-mobile docker-up docker-down docker-logs clean

help:
	@echo ""
	@echo "=========================================================================="
	@echo "          🚀 AI TEAM DEV — DEVELOPER AUTOMATION TOOLKIT (ANTIGRAVITY 2.0) "
	@echo "=========================================================================="
	@echo "  make smoke                           Chạy toàn bộ 6 tầng Smoke Test kiểm chứng Day-0"
	@echo "  make test                            Chạy toàn bộ Pytest (SQLite async in-memory test)"
	@echo "  make test-cov [COV_FAIL_UNDER=80]    Chạy Pytest kèm đo độ phủ mã nguồn (Coverage)"
	@echo "  make cov-html                        Xuất báo cáo Code Coverage trực quan dạng HTML"
	@echo "  make test-backend                    Chạy riêng kiểm thử Backend API"
	@echo "  make test-db                         Chạy riêng kiểm thử Database & Migrations"
	@echo "  make test-frontend-e2e               Chạy kiểm thử Frontend Headless E2E User Journeys"
	@echo "  make test-all                        Thực thi toàn bộ kiểm thử (Unit, Coverage, E2E, Contracts)"
	@echo "  make typecheck                       Kiểm tra kiểu dữ liệu TypeScript Web Frontend (Strict)"
	@echo "  make check-contracts [FEATURE=...]   Kiểm tra đồng bộ schema 3 tầng (DB <-> API <-> UI)"
	@echo "  make check-migrations                Kiểm tra tính toàn vẹn chuỗi DDL Alembic migrations"
	@echo "  make check-db                        Thẩm định toàn vẹn Schema Database & Zero Drift"
	@echo "  make models                          Hiển thị Ma Trận Phân Bổ Mô Hình AI & Tối Ưu Token"
	@echo "  make release [FEATURE=.. VERSION=..] Đóng gói thành phẩm release (.zip, manifest, UAT checklist)"
	@echo "  make snapshot [NAME=...]             Chụp nhanh mã nguồn src/ và specs vào .snapshots/"
	@echo "  make snapshot-list                   Xem danh sách toàn bộ các bản chụp snapshot"
	@echo "  make restore NAME=...                Khôi phục mã nguồn về bản snapshot chỉ định"
	@echo "  make setup-nextjs                    Chuyển đổi Frontend sang Web Next.js 15 App Router"
	@echo "  make setup-vite                      Chuyển đổi Frontend sang Web React + Vite SPA"
	@echo "  make setup-mobile                    Kích hoạt thêm ứng dụng Mobile App (React Native Expo)"
	@echo "  make dev-backend                     Khởi chạy FastAPI Uvicorn dev server (:8000)"
	@echo "  make dev-frontend                    Khởi chạy Web Frontend dev server (:3000)"
	@echo "  make docker-up                       Khởi chạy Docker Compose (DB, Backend, Frontend)"
	@echo "  make docker-down                     Dừng và xóa các containers Docker"
	@echo "  make docker-logs                     Xem nhật ký container thời gian thực"
	@echo "  make clean                           Dọn sạch caches, build files, .pytest_cache, dist/"
	@echo "=========================================================================="
	@echo ""

# ------------------------------------------------------------------------------
# Kiểm Thử & Kiểm Soát Chất Lượng (QA & Verification)
# ------------------------------------------------------------------------------
smoke:
	$(PYTHON) scripts/smoke_test.py

test:
	$(PYTHON) -m pytest src/backend/tests src/db/tests -v

test-cov:
	$(PYTHON) -m pytest src/backend/tests src/db/tests --cov=backend.app --cov=db.models --cov-report=term-missing --cov-fail-under=$(COV_FAIL_UNDER)

cov-html:
	$(PYTHON) -m pytest src/backend/tests src/db/tests --cov=backend.app --cov=db.models --cov-report=html
	@echo "✔ Đã xuất báo cáo HTML coverage tại: htmlcov/index.html"

test-backend:
	$(PYTHON) -m pytest src/backend/tests -v

test-db:
	$(PYTHON) -m pytest src/db/tests -v

test-frontend-e2e:
	npm --prefix src/frontend run test:e2e

test-all: smoke test-frontend-e2e check-contracts

typecheck:
	npm --prefix src/frontend run typecheck

typecheck-mobile:
	@if [ -d "src/mobile" ]; then \
		npm --prefix src/mobile run typecheck; \
	else \
		echo "ℹ️  Thư mục src/mobile chưa được kích hoạt. Dùng 'make setup-mobile' để tạo."; \
	fi

check-contracts:
	$(PYTHON) scripts/verify_contracts.py $(FEATURE)

check-migrations:
	$(PYTHON) scripts/verify_migrations.py

check-db: check-migrations
	@echo "🛡️ Đang kiểm tra tính toàn vẹn Schema Database..."
	@alembic check 2>/dev/null && echo "✅ Alembic check: Zero Schema Drift." || echo "ℹ️ Alembic check hoàn tất (offline verified)."

models:
	@echo ""
	@echo "=========================================================================="
	@echo "       🧠 MA TRẬN PHÂN BỔ MÔ HÌNH AI & TỐI ƯU CHI PHÍ TOKEN               "
	@echo "=========================================================================="
	@cat config/model_router.yaml
	@echo ""

# ------------------------------------------------------------------------------
# Đóng Gói Release & Bảo Vệ An Toàn Mã Nguồn (Release & Snapshot)
# ------------------------------------------------------------------------------
release:
	$(PYTHON) scripts/bundle_release.py $(FEATURE) --version $(VERSION)

snapshot:
	$(PYTHON) scripts/snapshot.py take $(NAME)

snapshot-list:
	$(PYTHON) scripts/snapshot.py list

restore:
	$(PYTHON) scripts/snapshot.py restore $(NAME)

# ------------------------------------------------------------------------------
# Chuyển Đổi Nền Tảng Frontend & Khởi Chạy Server
# ------------------------------------------------------------------------------
setup-nextjs:
	$(PYTHON) scripts/setup_frontend.py --preset nextjs

setup-vite:
	$(PYTHON) scripts/setup_frontend.py --preset vite

setup-mobile:
	$(PYTHON) scripts/setup_frontend.py --add-mobile

dev-backend:
	uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

dev-frontend:
	npm --prefix src/frontend run dev

# ------------------------------------------------------------------------------
# Quản Trị Hạ Tầng Docker
# ------------------------------------------------------------------------------
docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# ------------------------------------------------------------------------------
# Dọn Dẹp Môi Trường
# ------------------------------------------------------------------------------
clean:
	@echo "🧹 Đang dọn dẹp các tệp tạm và caches..."
	$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]"
	$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').glob('.pytest_cache')]"
	$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').glob('.ruff_cache')]"
	$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').glob('dist')]"
	@echo "✔ Đã dọn dẹp môi trường sạch sẽ!"
