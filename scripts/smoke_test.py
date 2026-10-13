#!/usr/bin/env python3
"""Day-0 Cross-Platform Smoke Verification Script for AI Team Dev.

Compatible with Windows, Linux, and macOS.
Executes:
1. Python Linting (Ruff)
2. Cross-Layer Contract Verification (scripts/verify_contracts.py)
3. Backend & DB Tests (Pytest SQLite In-Memory)
4. Frontend TypeScript (Strict Mode)

Usage:
    python scripts/smoke_test.py
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

# Ensure UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent


def get_python_executable() -> str:
    """Detect virtualenv Python executable across Windows, Linux, and macOS."""
    is_windows = platform.system() == "Windows"
    venv_dir = ROOT_DIR / ".venv"

    if is_windows:
        candidate = venv_dir / "Scripts" / "python.exe"
    else:
        candidate = venv_dir / "bin" / "python"

    if candidate.exists():
        return str(candidate)

    # Fallback to current running Python executable
    return sys.executable


def run_step(step_num: int, title: str, cmd: list[str], cwd: Path | None = None) -> bool:
    """Execute a single verification step and print results."""
    print(f"\n[{step_num}] {title}...")
    print(f"    Running: {' '.join(cmd)}")
    try:
        env = os.environ.copy()
        # Add src to PYTHONPATH cleanly across platforms
        src_path = str(ROOT_DIR / "src")
        existing_pythonpath = env.get("PYTHONPATH", "")
        if existing_pythonpath:
            env["PYTHONPATH"] = f"{src_path}{os.pathsep}{existing_pythonpath}"
        else:
            env["PYTHONPATH"] = src_path

        res = subprocess.run(cmd, cwd=str(cwd or ROOT_DIR), env=env, check=False)
        if res.returncode == 0:
            print(f"    ✅ {title}: PASSED")
            return True
        else:
            print(f"    ❌ {title}: FAILED (exit code {res.returncode})")
            return False
    except FileNotFoundError as e:
        print(f"    ❌ Executable not found for: {cmd[0]} ({e})")
        return False
    except Exception as e:
        print(f"    ❌ Unexpected error running {title}: {e}")
        return False


def main() -> int:
    print("=" * 72)
    print("🚀 AI Team Dev — Day-0 Cross-Platform Smoke Verification")
    print(f"   OS: {platform.system()} {platform.release()} | Architecture: {platform.machine()}")
    print("=" * 72)

    py_exe = get_python_executable()
    print(f"ℹ️ Using Python interpreter: {py_exe}")

    steps = [
        (1, "Python Linting (Ruff)", [py_exe, "-m", "ruff", "check", "src/"]),
        (2, "Cross-Layer Contract Verification", [py_exe, str(ROOT_DIR / "scripts" / "verify_contracts.py")]),
        (3, "Backend & DB Automated Tests (Pytest SQLite In-Memory)", [py_exe, "-m", "pytest", "src/backend/tests", "-v"]),
    ]

    # Frontend step
    is_windows = platform.system() == "Windows"
    npm_cmd = "npm.cmd" if is_windows else "npm"
    steps.append((4, "Frontend TypeScript Typecheck (Strict Mode)", [npm_cmd, "--prefix", "src/frontend", "run", "typecheck"]))

    all_passed = True
    for step_num, title, cmd in steps:
        success = run_step(step_num, title, cmd)
        if not success:
            all_passed = False
            break

    print("\n" + "=" * 72)
    if all_passed:
        print("🎉 ALL DAY-0 SMOKE VERIFICATION CHECKS PASSED 100%!")
        print("✨ Your workspace is ready for development on " + platform.system() + ".")
        print("=" * 72)
        return 0
    else:
        print("🚨 DAY-0 SMOKE VERIFICATION FAILED!")
        print("   Please check the error logs above and resolve any issues.")
        print("=" * 72)
        return 1


if __name__ == "__main__":
    sys.exit(main())
