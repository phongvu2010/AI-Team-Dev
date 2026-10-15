#!/usr/bin/env python3
"""Instant Snapshot & Safety Rollback Utility for AI Team Dev (Antigravity 2.0).

Allows developers to take sub-second snapshots of source code (`src/`),
specifications (`docs/specs/`), and configurations (`config/`) before major
AI refactors or new feature implementations, and instantly restore them if needed.

Usage:
    python scripts/snapshot.py take [snapshot_name]
    python scripts/snapshot.py list
    python scripts/snapshot.py restore <snapshot_name>
    python scripts/snapshot.py clean [--all]
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
SNAPSHOTS_DIR = ROOT_DIR / ".snapshots"

# Directories/files to ignore during snapshot
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


def should_include_file(file_path: Path) -> bool:
    """Filter out caches and temporary files."""
    for part in file_path.parts:
        if part in EXCLUDE_DIRS:
            return False
    if file_path.suffix in EXCLUDE_EXTS:
        return False
    return True


def copy_filtered_tree(src: Path, dst: Path):
    """Copy directory recursively skipping excluded files."""
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for root, dirs, files in os.walk(src):
        # Modify dirs in-place to avoid descending into excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        rel_root = Path(root).relative_to(src)
        target_root = dst / rel_root
        target_root.mkdir(parents=True, exist_ok=True)
        for f in files:
            src_file = Path(root) / f
            if should_include_file(src_file):
                shutil.copy2(src_file, target_root / f)


def take_snapshot(name: str | None = None) -> Path:
    """Create a new timestamped snapshot."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = (name or "vibe_checkpoint").strip().lower().replace(" ", "_")
    snapshot_folder = f"{safe_name}_{timestamp}"
    target_dir = SNAPSHOTS_DIR / snapshot_folder

    print(f"📸 Đang tạo bản chụp nhanh (Snapshot): '{snapshot_folder}'...")
    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Snapshot src/
    copy_filtered_tree(ROOT_DIR / "src", target_dir / "src")

    # 2. Snapshot docs/specs/
    copy_filtered_tree(ROOT_DIR / "docs" / "specs", target_dir / "docs" / "specs")

    # 3. Snapshot config/
    copy_filtered_tree(ROOT_DIR / "config", target_dir / "config")

    # 4. Save metadata
    meta_path = target_dir / "SNAPSHOT_META.txt"
    meta_path.write_text(
        f"Snapshot Name: {safe_name}\n"
        f"Created At: {datetime.now().isoformat()}\n"
        f"Timestamp: {timestamp}\n",
        encoding="utf-8",
    )

    print(f"✔ Đã lưu bản chụp thành công tại: {target_dir}")
    print(f"👉 Để khôi phục lại khi cần: python scripts/snapshot.py restore {snapshot_folder}")
    return target_dir


def list_snapshots():
    """List all available snapshots."""
    if not SNAPSHOTS_DIR.exists():
        print("ℹ️ Chưa có bản chụp snapshot nào được lưu.")
        return

    snapshots = [d for d in SNAPSHOTS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
    if not snapshots:
        print("ℹ️ Thư mục .snapshots/ đang rỗng.")
        return

    snapshots.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    print("\n" + "=" * 70)
    print("📋 DANH SÁCH CÁC BẢN CHỤP MÃ NGUỒN (AVAILABLE SNAPSHOTS)")
    print("=" * 70)
    for idx, s in enumerate(snapshots, 1):
        meta_file = s / "SNAPSHOT_META.txt"
        created_str = datetime.fromtimestamp(s.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{idx}] {s.name:<40} (Tạo lúc: {created_str})")
    print("=" * 70)
    print("👉 Lệnh khôi phục: python scripts/snapshot.py restore <snapshot_name>\n")


def restore_snapshot(target_name: str):
    """Restore source code from a snapshot with automatic safety backup."""
    if not SNAPSHOTS_DIR.exists():
        print("❌ Lỗi: Thư mục .snapshots/ không tồn tại.")
        sys.exit(1)

    matching = [d for d in SNAPSHOTS_DIR.iterdir() if d.is_dir() and target_name in d.name]
    if not matching:
        print(f"❌ Không tìm thấy snapshot nào khớp với từ khóa: '{target_name}'.")
        print("   Chạy 'python scripts/snapshot.py list' để xem danh sách.")
        sys.exit(1)

    selected_snapshot = matching[0]
    print(f"🔄 Đang chuẩn bị khôi phục từ snapshot: '{selected_snapshot.name}'...")

    # Safety step: Automatically take a safety snapshot of current state before overriding!
    print("🛡️ [Safety Precaution] Đang tự động lưu snapshot dự phòng trước khi khôi phục...")
    take_snapshot("pre_restore_backup")

    # Restore src/
    if (selected_snapshot / "src").exists():
        dest_src = ROOT_DIR / "src"
        if dest_src.exists():
            shutil.rmtree(dest_src)
        shutil.copytree(selected_snapshot / "src", dest_src)
        print("✔ Đã khôi phục: src/")

    # Restore docs/specs/
    if (selected_snapshot / "docs" / "specs").exists():
        dest_specs = ROOT_DIR / "docs" / "specs"
        if dest_specs.exists():
            shutil.rmtree(dest_specs)
        dest_specs.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(selected_snapshot / "docs" / "specs", dest_specs)
        print("✔ Đã khôi phục: docs/specs/")

    # Restore config/
    if (selected_snapshot / "config").exists():
        dest_config = ROOT_DIR / "config"
        if dest_config.exists():
            shutil.rmtree(dest_config)
        shutil.copytree(selected_snapshot / "config", dest_config)
        print("✔ Đã khôi phục: config/")

    print(f"\n🎉 KHÔI PHỤC THÀNH CÔNG toàn bộ mã nguồn về trạng thái của '{selected_snapshot.name}'!")


def clean_snapshots(keep_latest: int = 3):
    """Clean up older snapshots, keeping the latest N snapshots."""
    if not SNAPSHOTS_DIR.exists():
        return

    snapshots = [d for d in SNAPSHOTS_DIR.iterdir() if d.is_dir()]
    snapshots.sort(key=lambda d: d.stat().st_mtime, reverse=True)

    to_delete = snapshots[keep_latest:]
    if not to_delete:
        print(f"ℹ️ Số lượng snapshot ({len(snapshots)}) chưa vượt quá ngưỡng giữ lại ({keep_latest}).")
        return

    for s in to_delete:
        print(f"🗑️ Đang xóa snapshot cũ: {s.name}")
        shutil.rmtree(s, ignore_errors=True)
    print("✔ Đã dọn dẹp các snapshot cũ hoàn tất.")


def main():
    parser = argparse.ArgumentParser(description="Quản lý bản chụp nhanh mã nguồn (Snapshot & Rollback).")
    subparsers = parser.add_subparsers(dest="command", help="Lệnh thực hiện: take | list | restore | clean")

    take_parser = subparsers.add_parser("take", help="Tạo bản chụp snapshot mới.")
    take_parser.add_argument("name", nargs="?", default="checkpoint", help="Tên gợi nhớ cho snapshot.")

    subparsers.add_parser("list", help="Liệt kê toàn bộ snapshot hiện có.")

    restore_parser = subparsers.add_parser("restore", help="Khôi phục mã nguồn từ snapshot.")
    restore_parser.add_argument("name", help="Tên hoặc từ khóa của snapshot cần khôi phục.")

    clean_parser = subparsers.add_parser("clean", help="Dọn dẹp các snapshot cũ.")
    clean_parser.add_argument("--keep", type=int, default=3, help="Số lượng snapshot mới nhất cần giữ lại.")

    args = parser.parse_args()

    if args.command == "take":
        take_snapshot(args.name)
    elif args.command == "list":
        list_snapshots()
    elif args.command == "restore":
        restore_snapshot(args.name)
    elif args.command == "clean":
        clean_snapshots(args.keep)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
