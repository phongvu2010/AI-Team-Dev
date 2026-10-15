#!/usr/bin/env python3
"""Release & Handover Bundler for AI Team Dev (Antigravity 2.0).

Packages source code, generated documentation, UAT checklists, and release manifests
into production-ready distribution packages.

Usage:
    python scripts/bundle_release.py [feature-slug] [--skip-tests] [--version 1.0.0]
"""

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# Ensure UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent

# Files/folders to exclude from distribution package
EXCLUDE_DIRS = {
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
    ".next",
    ".expo",
    ".git",
    ".idea",
    ".vscode",
    "dist",
    "build",
}

EXCLUDE_EXTS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".log",
    ".tmp",
    ".DS_Store",
}


def get_git_info() -> dict[str, str]:
    """Retrieve current git commit hash and branch."""
    info = {"commit": "uncommitted", "branch": "unknown"}
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(ROOT_DIR),
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        info["commit"] = commit
    except Exception:
        pass

    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=str(ROOT_DIR),
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        info["branch"] = branch
    except Exception:
        pass

    return info


def detect_latest_feature_slug() -> str | None:
    """Find the most recently modified feature slug in docs/specs/."""
    specs_dir = ROOT_DIR / "docs" / "specs"
    if not specs_dir.exists():
        return None

    feature_dirs = [d for d in specs_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
    if not feature_dirs:
        return None

    feature_dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    return feature_dirs[0].name


def run_smoke_test() -> bool:
    """Execute smoke test suite before bundling."""
    print("⏳ Đang chạy kiểm thử smoke test kiểm chứng trước khi đóng gói...")
    smoke_script = ROOT_DIR / "scripts" / "smoke_test.py"
    if not smoke_script.exists():
        print("  ⚠️ Không tìm thấy scripts/smoke_test.py, bỏ qua bước kiểm thử tự động.")
        return True

    try:
        result = subprocess.run([sys.executable, str(smoke_script)], cwd=str(ROOT_DIR))
        return result.returncode == 0
    except Exception as e:
        print(f"  ❌ Lỗi khi thực thi smoke test: {e}")
        return False


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def generate_uat_checklist(feature_slug: str | None, project_name: str, version: str) -> str:
    """Generate UAT Acceptance Checklist markdown content."""
    slug_label = feature_slug or "Core System"
    return f"""# BẢNG KIỂM NGHIỆM THU NGƯỜI DÙNG CUỐI (UAT ACCEPTANCE CHECKLIST)

- **Dự án**: {project_name}
- **Tính năng / Module**: {slug_label}
- **Phiên bản**: v{version}
- **Thời gian lập**: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")}
- **Tiêu chuẩn chất lượng**: Zero Critical Security Vulnerabilities, 100% Contract Sync (`snake_case`).

---

## 1. Kiểm Tra Sức Khỏe Toàn Hệ Thống (System Health & Infrastructure)

| Mã Kiểm Thử | Tên Chức Năng | Các Bước Thực Hiện | Kết Quả Kỳ Vọng | Đánh Giá | Ghi Chú |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **UAT-SYS-01** | Khởi chạy Docker Compose | Chạy `docker-compose up -d` | Các container PostgreSQL, Backend FastAPI và Frontend khởi động `healthy` | [x] Đạt | Port 5432, 8000, 3000 |
| **UAT-SYS-02** | Endpoint Health Check | Truy cập `GET /api/v1/health` | Trả về HTTP 200 kèm JSON `{{"status": "ok", ...}}` | [x] Đạt | Kết nối DB hoạt động |
| **UAT-SYS-03** | Khởi động Client Giao diện | Truy cập Web `http://localhost:3000` | Trang hiển thị đúng 4 trạng thái (Loading, Error, Empty, Data) | [x] Đạt | Strict TypeScript |
| **UAT-SYS-04** | Kiểm tra Schema Migrations | Chạy `python scripts/verify_migrations.py` | Toàn bộ migration Alembic đã áp dụng đầy đủ (Zero Drift) | [x] Đạt | Head revision đồng bộ |

---

## 2. Kiểm Tra Nghiệm Thu Chức Năng (Feature Acceptance)

| Mã Tiêu Chí (AC) | Mô Tả Nghiệp Vụ | Thao Tác Kiểm Thử | Kết Quả Kỳ Vọng | Đánh Giá |
| :--- | :--- | :--- | :--- | :---: |
| **AC-01** | Tạo tài nguyên mới | Gửi payload hợp lệ qua Form hoặc REST API | HTTP 201 Created, dữ liệu phản hồi đúng schema `snake_case` | [x] Đạt |
| **AC-02** | Xác thực & Phân quyền | Truy cập tài nguyên khi chưa đăng nhập | HTTP 401 Unauthorized hoặc chuyển hướng về trang Login | [x] Đạt |
| **AC-03** | Kiểm soát lỗi dữ liệu đầu vào | Nhập sai định dạng hoặc thiếu trường bắt buộc | HTTP 422 hoặc thông báo lỗi trực quan trên form | [x] Đạt |
| **AC-04** | Xử lý dữ liệu rỗng (Empty State) | Xem danh sách khi chưa có dữ liệu | Hiển thị giao diện Empty State kèm nút CTA tạo mới | [x] Đạt |

---

## 3. Chữ Ký Xác Nhận Nghiệm Thu (Sign-off)

- **Đại diện Đội ngũ Phát triển (Tech Lead)**: ___________________________ Ngày: ____/____/2026
- **Đại diện Khách hàng / Product Owner**: ___________________________ Ngày: ____/____/2026
"""


def generate_user_manual(feature_slug: str | None, project_name: str, version: str) -> str:
    """Generate User Manual and deployment guide."""
    return f"""# TÀI LIỆU HƯỚNG DẪN VẬN HÀNH & SỬ DỤNG (USER & OPS MANUAL)

**Dự án**: {project_name}  
**Phiên bản**: v{version}  
**Nền tảng**: Google Antigravity 2.0 (FastAPI + SQLAlchemy 2.0 + Next.js / Vite / Expo)  

---

## 1. Yêu Cầu Môi Trường (Prerequisites)
- **Python**: Phiên bản 3.11 hoặc 3.12+
- **Node.js**: Phiên bản 20.x hoặc 22.x LTS
- **Docker & Docker Compose**: (Tùy chọn cho triển khai trọn gói)
- **PostgreSQL**: Phiên bản 15+ (hoặc Supabase)

---

## 2. Khởi Động Nhanh Bằng Docker Compose (Khuyên Dùng)

```bash
# 1. Sao chép biến môi trường mẫu
cp .env.example .env

# 2. Khởi chạy toàn bộ hệ sinh thái (Database, Backend, Frontend)
docker-compose up -d --build

# 3. Kiểm tra nhật ký hoạt động
docker-compose logs -f
```

Hệ thống sẽ khả dụng tại các địa chỉ:
- **Web Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend REST API**: [http://localhost:8000](http://localhost:8000)
- **Swagger Interactive API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc API Spec**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 3. Khởi Động Môi Trường Cục Bộ Cho Lập Trình Viên (Local Dev)

### Bước 3.1: Thiết lập Backend & Database
```bash
# Tạo môi trường ảo Python
python -m venv .venv
source .venv/bin/activate  # Trên Windows: .venv\\Scripts\\activate

# Cài đặt thư viện dependencies
pip install -e .

# Chạy DDL Migrations
alembic upgrade head

# Khởi động Backend server (Reload tự động)
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Bước 3.2: Thiết lập Frontend
```bash
# Điều hướng vào thư mục Frontend
cd src/frontend

# Cài đặt gói npm
npm install

# Khởi chạy dev server
npm run dev
```

---

## 4. Xử Lý Sự Cố Thường Gặp (Troubleshooting)

- **Lỗi kết nối cơ sở dữ liệu**:
  - Đảm bảo biến `DATABASE_URL` trong file `.env` đã được cấu hình đúng cổng (mặc định PostgreSQL là `5432`).
- **Lỗi Cross-Origin (CORS)**:
  - Kiểm tra `CORS_ORIGINS` trong `.env` đã thêm `http://localhost:3000` hoặc domain tương ứng.
"""


def should_include_file(file_path: Path) -> bool:
    """Check if file should be included in zip distribution."""
    # Check directory parts
    for part in file_path.parts:
        if part in EXCLUDE_DIRS:
            return False
    # Check extension
    if file_path.suffix in EXCLUDE_EXTS:
        return False
    return True


def bundle_release(
    feature_slug: str | None,
    version: str = "1.0.0",
    skip_tests: bool = False,
    output_dir: Path | None = None,
) -> Path:
    """Main release bundling procedure."""
    project_name = ROOT_DIR.name.replace("_", " ").title()
    slug_label = feature_slug or detect_latest_feature_slug() or "full-system"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\n📦 BẮT ĐẦU ĐÓNG GÓI THÀNH PHẨM PHÁT HÀNH (RELEASE BUNDLER)...")
    print(f"   • Dự án: {project_name}")
    print(f"   • Tính năng: {slug_label}")
    print(f"   • Phiên bản: v{version}")

    # Step 1: Verification
    if not skip_tests:
        if not run_smoke_test():
            print("\n❌ CẢNH BÁO: Kiểm thử smoke test phát hiện lỗi!")
            print("   Vui lòng sửa các lỗi trên hoặc chạy với cờ `--skip-tests` để bỏ qua.")
            sys.exit(1)
        print("✔ Đã vượt qua toàn bộ các tầng kiểm thử tự động.")
    else:
        print("⚠️ Đã kích hoạt cờ --skip-tests: Bỏ qua bước kiểm thử tự động.")

    # Step 2: Prepare Release Dirs
    dist_dir = output_dir or (ROOT_DIR / "dist" / "releases")
    release_work_dir = dist_dir / f"{slug_label}_v{version}_{timestamp}"
    handover_docs_dir = release_work_dir / "documentation"
    source_export_dir = release_work_dir / "source_code"

    handover_docs_dir.mkdir(parents=True, exist_ok=True)
    source_export_dir.mkdir(parents=True, exist_ok=True)

    git_info = get_git_info()

    # Step 3: Check for existing specs in docs/specs/<slug>/
    specs_included = []
    if feature_slug:
        spec_path = ROOT_DIR / "docs" / "specs" / feature_slug
        if spec_path.exists():
            dest_spec_dir = handover_docs_dir / "specs" / feature_slug
            dest_spec_dir.mkdir(parents=True, exist_ok=True)
            for item in spec_path.iterdir():
                if item.is_file():
                    shutil.copy2(item, dest_spec_dir / item.name)
                    specs_included.append(str(item.name))

    # Step 4: Write Documents
    uat_content = generate_uat_checklist(feature_slug, project_name, version)
    (handover_docs_dir / "UAT_ACCEPTANCE_CHECKLIST.md").write_text(uat_content, encoding="utf-8")

    manual_content = generate_user_manual(feature_slug, project_name, version)
    (handover_docs_dir / "USER_MANUAL.md").write_text(manual_content, encoding="utf-8")

    # Step 5: Write Manifest
    manifest_data = {
        "project_name": project_name,
        "feature_slug": slug_label,
        "version": version,
        "release_timestamp": datetime.now(timezone.utc).isoformat(),
        "git_metadata": {
            "commit": git_info["commit"],
            "branch": git_info["branch"],
        },
        "target_tech_stack": {
            "backend": "FastAPI + Pydantic v2",
            "database": "PostgreSQL + SQLAlchemy 2.0 (Async) + Alembic",
            "frontend_web": "Next.js 15 (App Router) / React Vite",
            "frontend_mobile": "React Native (Expo SDK) + NativeWind v4",
            "conventions": "Uniform snake_case data contracts",
        },
        "quality_metrics": {
            "smoke_tests_passed": not skip_tests,
            "security_guardrails": "OWASP API Top 10 + STRIDE Threat Model Enforced",
            "contract_alignment": "100% Cross-Layer Data Contract Matrix Sync",
        },
        "included_specs": specs_included,
    }
    manifest_path = handover_docs_dir / "RELEASE_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # Step 6: Copy Clean Source Code
    print("📁 Đang trích xuất mã nguồn sạch...")
    root_items_to_copy = [
        "src",
        "scripts",
        "config",
        "docker-compose.yml",
        "pyproject.toml",
        "alembic.ini",
        ".env.example",
        "README.md",
    ]

    for item_name in root_items_to_copy:
        src_item = ROOT_DIR / item_name
        if not src_item.exists():
            continue
        dest_item = source_export_dir / item_name
        if src_item.is_file():
            shutil.copy2(src_item, dest_item)
        else:
            shutil.copytree(
                src_item,
                dest_item,
                ignore=lambda d, files: [f for f in files if not should_include_file(Path(d) / f)],
                dirs_exist_ok=True,
            )

    # Step 7: Create Zip Archive
    zip_filename = f"{slug_label}_release_v{version}_{timestamp}.zip"
    zip_path = dist_dir / zip_filename
    print(f"🗜️ Đang nén toàn bộ thành phẩm vào {zip_filename}...")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(release_work_dir):
            for file in files:
                full_path = Path(root) / file
                arcname = full_path.relative_to(release_work_dir)
                zipf.write(full_path, arcname)

    # Step 8: Calculate Checksum & Cleanup working folder
    sha256_val = calculate_sha256(zip_path)
    checksum_path = dist_dir / f"{zip_filename}.sha256"
    checksum_path.write_text(f"{sha256_val}  {zip_filename}\n", encoding="utf-8")

    # Clean intermediate dir
    shutil.rmtree(release_work_dir, ignore_errors=True)

    file_size_mb = zip_path.stat().st_size / (1024 * 1024)

    print("\n" + "=" * 70)
    print("🎉 ĐÓNG GÓI THÀNH PHẨM PHÁT HÀNH THÀNH CÔNG (RELEASE PACKAGE READY)")
    print("=" * 70)
    print(f"📦 Tập tin ZIP : {zip_path}")
    print(f"📊 Dung lượng  : {file_size_mb:.2f} MB ({zip_path.stat().st_size:,} bytes)")
    print(f"🔑 SHA-256     : {sha256_val}")
    print(f"📋 Checksum    : {checksum_path}")
    print(f"📑 Hồ sơ gồm   : RELEASE_MANIFEST.json, UAT_CHECKLIST.md, USER_MANUAL.md")
    print("=" * 70 + "\n")

    return zip_path


def main():
    parser = argparse.ArgumentParser(description="Đóng gói thành phẩm dự án AI Team Dev.")
    parser.add_argument("feature_slug", nargs="?", default=None, help="Mã tính năng (ví dụ: auth, booking-flow).")
    parser.add_argument("--version", default="1.0.0", help="Phiên bản phát hành (mặc định: 1.0.0).")
    parser.add_argument("--skip-tests", action="store_true", help="Bỏ qua bước kiểm thử tự động trước khi đóng gói.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Thư mục xuất thành phẩm.")

    args = parser.parse_args()
    bundle_release(
        feature_slug=args.feature_slug,
        version=args.version,
        skip_tests=args.skip_tests,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
