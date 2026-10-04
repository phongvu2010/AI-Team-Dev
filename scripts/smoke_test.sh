#!/usr/bin/env bash
# Day-0 Smoke Verification Script for AI Team Dev (Antigravity 2.0)
set -e

echo "======================================================================"
echo "🚀 Running AI Team Dev — Day-0 Smoke Verification"
echo "======================================================================"

echo ""
echo "1️⃣ Checking Python Linting (Ruff)..."
.venv/bin/ruff check src/
echo "   ✅ Ruff checks passed!"

echo ""
echo "2️⃣ Running Backend & DB Tests (Pytest SQLite In-Memory)..."
PYTHONPATH=src .venv/bin/pytest src/backend/tests -v
echo "   ✅ Pytest passed!"

echo ""
echo "3️⃣ Checking Frontend TypeScript (Strict Mode)..."
npm --prefix src/frontend run typecheck
echo "   ✅ Frontend Typecheck passed!"

echo ""
echo "======================================================================"
echo "🎉 ALL DAY-0 SMOKE CHECKS PASSED 100%!"
echo "======================================================================"
