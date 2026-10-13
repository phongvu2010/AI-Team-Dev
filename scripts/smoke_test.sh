#!/usr/bin/env bash
# Day-0 Smoke Verification Script for AI Team Dev (Cross-Platform Bash)
set -e

echo "======================================================================"
echo "🚀 Running AI Team Dev — Day-0 Smoke Verification (Bash)"
echo "======================================================================"

# Locate Python in .venv (Linux/macOS .venv/bin vs Windows Git Bash .venv/Scripts) or PATH
if [ -f ".venv/bin/python" ]; then
    PY=".venv/bin/python"
elif [ -f ".venv/Scripts/python.exe" ]; then
    PY=".venv/Scripts/python.exe"
elif command -v python3 >/dev/null 2>&1; then
    PY="python3"
else
    PY="python"
fi

echo "ℹ️ Using Python interpreter: $PY"
echo ""

echo "1️⃣ Checking Python Linting (Ruff)..."
$PY -m ruff check src/
echo "   ✅ Ruff checks passed!"

echo ""
echo "2️⃣ Verifying Cross-Layer Contracts..."
$PY scripts/verify_contracts.py
echo "   ✅ Contract verification passed!"

echo ""
echo "3️⃣ Running Backend & DB Tests (Pytest SQLite In-Memory)..."
$PY -m pytest src/backend/tests -v
echo "   ✅ Pytest passed!"

echo ""
echo "4️⃣ Checking Frontend TypeScript (Strict Mode)..."
npm --prefix src/frontend run typecheck
echo "   ✅ Frontend Typecheck passed!"

echo ""
echo "======================================================================"
echo "🎉 ALL DAY-0 SMOKE CHECKS PASSED 100%!"
echo "======================================================================"
