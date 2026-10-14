#!/usr/bin/env python3
"""Local Development Server Runner for AI Team Dev (`scripts/start_dev.py`).

Starts both Backend (FastAPI @ port 8000) and Frontend (Next.js/Vite @ port 3000/5173)
concurrently with unified log streaming, graceful shutdown, and seamless integration
with Antigravity 2.0's `/browser` visual testing.

Usage:
    python scripts/start_dev.py                 # Live mode (Next.js + FastAPI)
    python scripts/start_dev.py --mode mock     # Mock mode (NEXT_PUBLIC_USE_MOCKS=true)
    python scripts/start_dev.py --backend-only  # Run FastAPI only
    python scripts/start_dev.py --frontend-only # Run Frontend only
    python scripts/start_dev.py --check         # Check network ports and exit
"""

import argparse
import os
import platform
import signal
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

# Ensure UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "src" / "frontend"


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

    return sys.executable


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Check if a TCP port is currently in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


def detect_frontend_framework() -> tuple[str, int]:
    """Detect framework and default port for src/frontend."""
    pkg_json = FRONTEND_DIR / "package.json"
    if pkg_json.exists():
        try:
            content = pkg_json.read_text(encoding="utf-8")
            if '"next"' in content:
                return "Next.js 15 App Router", 3000
            elif '"vite"' in content:
                return "React Vite SPA", 5173
        except Exception:
            pass
    return "Web Frontend", 3000


def stream_output(process: subprocess.Popen, prefix: str) -> None:
    """Stream process stdout/stderr with a colored/formatted prefix."""
    try:
        for line in iter(process.stdout.readline, ""):
            if not line:
                break
            print(f"{prefix} {line.rstrip()}")
    except (ValueError, OSError):
        pass


def kill_process_tree(proc: subprocess.Popen | None) -> None:
    """Safely terminate a process and all its child processes across platforms."""
    if proc is None or proc.poll() is not None:
        return

    pid = proc.pid
    is_windows = platform.system() == "Windows"

    try:
        if is_windows:
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        else:
            proc.terminate()
            proc.wait(timeout=2.0)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Start development servers for AI Team Dev.")
    parser.add_argument(
        "--mode",
        choices=["live", "mock"],
        default="live",
        help="Run frontend in live mode (backend API) or mock mode (fixtures)",
    )
    parser.add_argument("--backend-only", action="store_true", help="Start only Backend FastAPI server")
    parser.add_argument("--frontend-only", action="store_true", help="Start only Frontend Web server")
    parser.add_argument("--check", action="store_true", help="Check port availability and exit")
    parser.add_argument("--backend-port", type=int, default=8000, help="Backend port (default: 8000)")
    parser.add_argument("--frontend-port", type=int, default=None, help="Frontend port override")

    args = parser.parse_args()

    fw_name, default_fe_port = detect_frontend_framework()
    frontend_port = args.frontend_port or default_fe_port

    print("=" * 72)
    print("🚀 AI Team Dev — Local Development Servers")
    print(f"   Mode: {args.mode.upper()} | Frontend: {fw_name}")
    print("=" * 72)

    if args.check:
        print("\n🔍 Port Availability Check:")
        be_used = is_port_in_use(args.backend_port)
        fe_used = is_port_in_use(frontend_port)
        print(f"   • Backend Port {args.backend_port}: {'🔴 BUSY' if be_used else '🟢 FREE'}")
        print(f"   • Frontend Port {frontend_port}: {'🔴 BUSY' if fe_used else '🟢 FREE'}")
        return 0

    py_exe = get_python_executable()
    is_windows = platform.system() == "Windows"
    npm_cmd = "npm.cmd" if is_windows else "npm"

    procs: list[subprocess.Popen] = []

    def shutdown(signum=None, frame=None):
        print("\n\n🛑 Shutting down development servers...")
        for p in procs:
            kill_process_tree(p)
        print("✨ All servers stopped cleanly.")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, shutdown)

    # 1. Start Backend FastAPI
    if not args.frontend_only:
        if is_port_in_use(args.backend_port):
            print(f"⚠️ Warning: Port {args.backend_port} is already in use. Backend might fail to bind.")

        backend_env = os.environ.copy()
        src_dir = str(ROOT_DIR / "src")
        backend_env["PYTHONPATH"] = (
            f"{src_dir}{os.pathsep}{backend_env.get('PYTHONPATH', '')}"
            if backend_env.get("PYTHONPATH")
            else src_dir
        )

        backend_cmd = [
            py_exe,
            "-m",
            "uvicorn",
            "backend.app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(args.backend_port),
            "--reload",
        ]
        print(f"🔧 Starting Backend (FastAPI @ http://localhost:{args.backend_port})...")
        be_proc = subprocess.Popen(
            backend_cmd,
            cwd=str(ROOT_DIR),
            env=backend_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        procs.append(be_proc)
        threading.Thread(target=stream_output, args=(be_proc, "[BACKEND]"), daemon=True).start()

    # 2. Start Frontend
    if not args.backend_only:
        if is_port_in_use(frontend_port):
            print(f"⚠️ Warning: Port {frontend_port} is already in use. Frontend might choose an alternate port.")

        frontend_env = os.environ.copy()
        if args.mode == "mock":
            frontend_env["NEXT_PUBLIC_USE_MOCKS"] = "true"
            frontend_env["VITE_USE_MOCKS"] = "true"
        else:
            frontend_env["NEXT_PUBLIC_USE_MOCKS"] = "false"
            frontend_env["VITE_USE_MOCKS"] = "false"

        frontend_cmd = [npm_cmd, "--prefix", "src/frontend", "run", "dev"]
        print(f"🎨 Starting Frontend ({fw_name} @ http://localhost:{frontend_port})...")
        fe_proc = subprocess.Popen(
            frontend_cmd,
            cwd=str(ROOT_DIR),
            env=frontend_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        procs.append(fe_proc)
        threading.Thread(target=stream_output, args=(fe_proc, "[FRONTEND]"), daemon=True).start()

    time.sleep(2)

    print("\n" + "=" * 72)
    print("🌐 ACTIVE SERVICES & ACCESS URLS:")
    if not args.frontend_only:
        print(f"   • Backend API Docs:   http://localhost:{args.backend_port}/docs")
        print(f"   • Backend Health:     http://localhost:{args.backend_port}/health")
    if not args.backend_only:
        print(f"   • Frontend Web App:   http://localhost:{frontend_port}")
        print("\n💡 For Visual Testing & UI Verification in Antigravity Chat:")
        print(f"   👉 Run slash command: /browser http://localhost:{frontend_port}")
    print("=" * 72)
    print("Press Ctrl+C to stop all servers.\n")

    try:
        while True:
            time.sleep(1)
            # Check if any process died unexpectedly
            for p in procs:
                if p.poll() is not None:
                    print(f"\n⚠️ A server process exited with code {p.returncode}.")
                    shutdown()
    except KeyboardInterrupt:
        shutdown()

    return 0


if __name__ == "__main__":
    sys.exit(main())
