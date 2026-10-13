# Day-0 Smoke Verification Script for Windows PowerShell
# Requires: .venv or python available in PATH
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Running AI Team Dev - Day-0 Smoke Verification (Windows PowerShell)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Locate Python in .venv or PATH
$PyExe = if (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
Write-Host "Using Python: $PyExe`n" -ForegroundColor Gray

Write-Host "[1/4] Checking Python Linting (Ruff)..." -ForegroundColor Yellow
& $PyExe -m ruff check src/
if ($LASTEXITCODE -ne 0) { throw "Ruff linting failed." }
Write-Host "   [OK] Ruff checks passed!`n" -ForegroundColor Green

Write-Host "[2/4] Verifying Cross-Layer Contracts..." -ForegroundColor Yellow
& $PyExe scripts/verify_contracts.py
if ($LASTEXITCODE -ne 0) { throw "Contract verification failed." }
Write-Host "   [OK] Contract verification passed!`n" -ForegroundColor Green

Write-Host "[3/4] Running Backend and DB Tests (Pytest SQLite In-Memory)..." -ForegroundColor Yellow
& $PyExe -m pytest src/backend/tests -v
if ($LASTEXITCODE -ne 0) { throw "Pytest execution failed." }
Write-Host "   [OK] Pytest passed!`n" -ForegroundColor Green

Write-Host "[4/4] Checking Frontend TypeScript (Strict Mode)..." -ForegroundColor Yellow
npm.cmd --prefix src/frontend run typecheck
if ($LASTEXITCODE -ne 0) { throw "Frontend typecheck failed." }
Write-Host "   [OK] Frontend Typecheck passed!`n" -ForegroundColor Green

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "ALL DAY-0 SMOKE CHECKS PASSED 100%!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
