"""Automated tests for Alembic migrations integrity, DAG continuity, and offline migration generator."""

import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

from db.migrations.generate_offline_migration import create_migration

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from verify_migrations import verify_alembic_structure, verify_migration_chain  # noqa: E402


def test_alembic_structure_and_assets() -> None:
    """Verify that alembic.ini, env.py, and script.py.mako exist and have valid syntax."""
    errors = verify_alembic_structure()
    assert not errors, f"Alembic structural errors detected: {errors}"


def test_migration_chain_integrity() -> None:
    """Verify that all existing migration files in versions/ form a valid DAG without breaks or cycles."""
    _, errors = verify_migration_chain()
    assert not errors, f"Migration chain integrity errors detected: {errors}"


def test_generate_offline_migration_creates_valid_file() -> None:
    """Verify that generate_offline_migration creates a syntactically valid Python migration script."""
    test_slug = "test_smoke_schema"
    created_path_str = create_migration(test_slug)
    created_path = Path(created_path_str)

    try:
        assert created_path.exists(), "Generated migration file does not exist on disk."
        assert created_path.suffix == ".py"

        # Check Python syntax via ast.parse
        content = created_path.read_text(encoding="utf-8")
        parsed = ast.parse(content, filename=str(created_path))
        assert parsed is not None

        # Verify revision metadata in generated file
        assert "revision: str =" in content or "revision =" in content
        assert "down_revision:" in content
        assert "def upgrade() -> None:" in content
        assert "def downgrade() -> None:" in content

        # Verify migration chain passes with the new file
        migrations, errors = verify_migration_chain()
        assert not errors, f"Migration chain broken after generating migration: {errors}"
        assert any(m["path"] == created_path for m in migrations)
    finally:
        # Clean up test migration file to maintain pristine workspace
        if created_path.exists():
            created_path.unlink()


@pytest.mark.postgres_only
def test_alembic_upgrade_downgrade_cycle() -> None:
    """Verify reversible DDL execution (upgrade head -> downgrade base -> upgrade head).

    Only executes when TEST_DATABASE_URL points to a live PostgreSQL instance.
    """
    test_db_url = os.getenv("TEST_DATABASE_URL")
    if not test_db_url or not test_db_url.startswith("postgresql"):
        pytest.skip("Requires live PostgreSQL in TEST_DATABASE_URL")

    env = os.environ.copy()
    env["DIRECT_DATABASE_URL"] = test_db_url

    # 1. Upgrade to head
    res_up = subprocess.run(["alembic", "upgrade", "head"], env=env, capture_output=True, text=True)
    assert res_up.returncode == 0, f"Alembic upgrade head failed: {res_up.stderr}"

    # 2. Downgrade to base
    res_down = subprocess.run(["alembic", "downgrade", "base"], env=env, capture_output=True, text=True)
    assert res_down.returncode == 0, f"Alembic downgrade base failed: {res_down.stderr}"

    # 3. Re-upgrade to head
    res_reup = subprocess.run(["alembic", "upgrade", "head"], env=env, capture_output=True, text=True)
    assert res_reup.returncode == 0, f"Alembic re-upgrade head failed: {res_reup.stderr}"
