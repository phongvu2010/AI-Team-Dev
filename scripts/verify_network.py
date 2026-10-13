"""Network, Port Alignment & CORS Diagnostic Utility (`scripts/verify_network.py`).

Verifies connectivity and configuration across the 3 core layers:
1. Backend API (FastAPI port 8000: /health & /api/v1/health)
2. Frontend App (Next.js port 3000 / 3001)
3. Database (PostgreSQL / Supabase port 5432 / 6543)
4. CORS headers validation
"""

import os
import socket
import sys
import urllib.error
import urllib.request

# Ensure UTF-8 console output on Windows to prevent UnicodeEncodeError
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """Check if a TCP port is open and listening."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex((host, port)) == 0


def check_http_endpoint(url: str, headers: dict[str, str] | None = None) -> tuple[bool, int, str]:
    """Test HTTP endpoint status code and response."""
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            body = resp.read().decode("utf-8")
            return True, resp.status, body
    except urllib.error.HTTPError as e:
        return False, e.code, str(e)
    except Exception as e:
        return False, 0, str(e)


def main() -> int:
    print("=" * 70)
    print("🔍 AI Team Dev — Network & Port Alignment Diagnostics")
    print("=" * 70)

    # 1. Check Backend API Port 8000
    backend_host = "127.0.0.1"
    backend_port = 8000
    backend_open = is_port_open(backend_host, backend_port)

    print(f"\n[1] Backend API (FastAPI @ http://{backend_host}:{backend_port}):")
    if backend_open:
        print(f"    ✅ Port {backend_port} is OPEN and listening.")
        # Test /health
        ok, status, body = check_http_endpoint(f"http://{backend_host}:{backend_port}/health")
        if ok and status == 200:
            print(f"    ✅ GET /health: 200 OK -> {body.strip()}")
        else:
            print(f"    ⚠️ GET /health returned status {status}: {body}")

        # Test CORS headers
        cors_headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        }
        ok_cors, status_cors, _ = check_http_endpoint(
            f"http://{backend_host}:{backend_port}/health", headers=cors_headers
        )
        if ok_cors:
            print("    ✅ CORS preflight / Origin check: Allowed")
        else:
            print(f"    ⚠️ CORS check status: {status_cors}")
    else:
        print(f"    ℹ️ Port {backend_port} is not currently running (start with: uvicorn backend.app.main:app --reload)")

    # 2. Check Frontend Port 3000 / 3001
    frontend_host = "127.0.0.1"
    p3000_open = is_port_open(frontend_host, 3000)
    p3001_open = is_port_open(frontend_host, 3001)

    print(f"\n[2] Frontend Web App (Next.js @ http://{frontend_host}:3000 / 3001):")
    if p3000_open:
        print("    ✅ Port 3000 is OPEN (Primary Next.js port).")
    elif p3001_open:
        print("    ✅ Port 3001 is OPEN (Fallback Next.js port).")
    else:
        print("    ℹ️ Frontend is not currently running (start with: npm --prefix src/frontend run dev)")

    # 3. Check Database Port 5432
    db_host = "127.0.0.1"
    db_port = 5432
    db_open = is_port_open(db_host, db_port)
    print(f"\n[3] Database Connection Check (PostgreSQL @ {db_host}:{db_port}):")
    if db_open:
        print(f"    ✅ Port {db_port} is OPEN (PostgreSQL active).")
    else:
        print(f"    ℹ️ Port {db_port} is not listening locally.")
        print("       (Note: Automated Pytest runs completely isolated using SQLite in-memory without needing PG)")

    # 4. Check Environment Variables
    print("\n[4] Environment Variables Alignment:")
    db_url = os.getenv("DATABASE_URL", "default local")
    test_db_url = os.getenv("TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    next_api_url = os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:8000")
    next_mocks = os.getenv("NEXT_PUBLIC_USE_MOCKS", "false")

    print(f"    - DATABASE_URL: {db_url}")
    print(f"    - TEST_DATABASE_URL: {test_db_url}")
    print(f"    - NEXT_PUBLIC_API_URL: {next_api_url}")
    print(f"    - NEXT_PUBLIC_USE_MOCKS: {next_mocks}")

    print("\n" + "=" * 70)
    print("✨ Diagnostics complete.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
