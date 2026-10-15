<#
.SYNOPSIS
    Bo tu dong hoa lenh 1-cham cho AI Team Dev tren Windows PowerShell.
.EXAMPLE
    .\run.ps1 smoke
    .\run.ps1 test
    .\run.ps1 release [feature-slug]
    .\run.ps1 snapshot [name]
    .\run.ps1 restore <name>
    .\run.ps1 clean
#>

param(
    [Parameter(Position=0)]
    [string]$Command = "help",

    [Parameter(Position=1)]
    [string]$Arg1 = "",

    [Parameter(Position=2)]
    [string]$Arg2 = ""
)

$ErrorActionPreference = "Stop"

# Detect Python interpreter in virtual environment
$Python = "python"
if (Test-Path ".venv\Scripts\python.exe") {
    $Python = ".venv\Scripts\python.exe"
}

switch ($Command.ToLower()) {
    "smoke" {
        & $Python scripts/smoke_test.py
    }
    "test" {
        & $Python -m pytest src/backend/tests src/db/tests -v
    }
    "test-backend" {
        & $Python -m pytest src/backend/tests -v
    }
    "test-db" {
        & $Python -m pytest src/db/tests -v
    }
    "typecheck" {
        npm.cmd --prefix src/frontend run typecheck
    }
    "check-contracts" {
        if ($Arg1) {
            & $Python scripts/verify_contracts.py $Arg1
        } else {
            & $Python scripts/verify_contracts.py
        }
    }
    "check-migrations" {
        & $Python scripts/verify_migrations.py
    }
    "release" {
        if ($Arg1) {
            & $Python scripts/bundle_release.py $Arg1
        } else {
            & $Python scripts/bundle_release.py
        }
    }
    "snapshot" {
        if ($Arg1) {
            & $Python scripts/snapshot.py take $Arg1
        } else {
            & $Python scripts/snapshot.py take
        }
    }
    "snapshot-list" {
        & $Python scripts/snapshot.py list
    }
    "restore" {
        if (-not $Arg1) {
            Write-Host 'Vui long chi dinh ten snapshot can khoi phuc. Vi du: .\run.ps1 restore <name>' -ForegroundColor Red
            exit 1
        }
        & $Python scripts/snapshot.py restore $Arg1
    }
    "setup-nextjs" {
        & $Python scripts/setup_frontend.py --preset nextjs
    }
    "setup-vite" {
        & $Python scripts/setup_frontend.py --preset vite
    }
    "setup-mobile" {
        & $Python scripts/setup_frontend.py --add-mobile
    }
    "dev-backend" {
        & $Python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
    }
    "dev-frontend" {
        npm.cmd --prefix src/frontend run dev
    }
    "docker-up" {
        docker-compose up -d --build
    }
    "docker-down" {
        docker-compose down
    }
    "docker-logs" {
        docker-compose logs -f
    }
    "clean" {
        Write-Host 'Dang don dep cac tep tam va caches...' -ForegroundColor Cyan
        Get-ChildItem -Path . -Include __pycache__, .pytest_cache, .ruff_cache, dist -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host 'Da don dep moi truong sach se!' -ForegroundColor Green
    }
    default {
        Write-Host ''
        Write-Host '==========================================================================' -ForegroundColor Cyan
        Write-Host '          AI TEAM DEV - WINDOWS POWERSHELL RUNNER (ANTIGRAVITY 2.0)       ' -ForegroundColor Yellow
        Write-Host '==========================================================================' -ForegroundColor Cyan
        Write-Host '  .\run.ps1 smoke                           Chay 5 tang Smoke Test Day-0'
        Write-Host '  .\run.ps1 test                            Chay Pytest (SQLite in-memory)'
        Write-Host '  .\run.ps1 typecheck                       Kiem tra kieu du lieu TypeScript'
        Write-Host '  .\run.ps1 check-contracts [slug]          Kiem tra dong bo schema 3 tang'
        Write-Host '  .\run.ps1 check-migrations                Kiem tra toan ven Alembic migrations'
        Write-Host '  .\run.ps1 release [slug]                  Dong goi phat hanh ZIP, Manifest, UAT'
        Write-Host '  .\run.ps1 snapshot [name]                 Chup nhanh ma nguon src/ va specs'
        Write-Host '  .\run.ps1 snapshot-list                   Xem danh sach ban chup snapshot'
        Write-Host '  .\run.ps1 restore <name>                  Khoi phuc ma nguon ve ban snapshot'
        Write-Host '  .\run.ps1 setup-nextjs / setup-vite       Chuyen doi Frontend Next.js / Vite'
        Write-Host '  .\run.ps1 setup-mobile                    Kich hoat them Mobile App Expo'
        Write-Host '  .\run.ps1 dev-backend / dev-frontend      Khoi chay dev server cuc bo'
        Write-Host '  .\run.ps1 clean                           Don dep caches va temporary files'
        Write-Host '==========================================================================' -ForegroundColor Cyan
        Write-Host ''
    }
}
