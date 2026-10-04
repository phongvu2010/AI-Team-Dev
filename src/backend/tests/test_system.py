"""System smoke tests verifying API and in-memory async SQLite database fixtures."""

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_health_check_endpoint(async_client: AsyncClient) -> None:
    """Verify FastAPI /health and /api/v1/health return 200 OK and status ok."""
    for path in ("/health", "/api/v1/health"):
        response = await async_client.get(path)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


@pytest.mark.asyncio
async def test_in_memory_db_session(async_db_session: AsyncSession) -> None:
    """Verify async SQLite fallback session can execute SQL queries."""
    result = await async_db_session.execute(text("SELECT 1 AS num"))
    row = result.scalar_one()
    assert row == 1


@pytest.mark.asyncio
async def test_client_fixture_with_db(client: AsyncClient, async_db_session: AsyncSession) -> None:
    """Verify `client` fixture works with automatic get_db_session override."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    result = await async_db_session.execute(text("SELECT 42 AS answer"))
    assert result.scalar_one() == 42


@pytest.mark.asyncio
async def test_db_dialect_fixture(db_dialect: str) -> None:
    """Verify db_dialect fixture identifies sqlite or postgresql correctly."""
    assert db_dialect in ("sqlite", "postgresql")


@pytest.mark.asyncio
@pytest.mark.postgres_only
async def test_postgres_only_marker_skips_on_sqlite(async_db_session: AsyncSession) -> None:
    """Verify postgres_only test runs when on PostgreSQL or skips cleanly on SQLite."""
    # When on PostgreSQL, version() is a valid function. On SQLite this is automatically skipped.
    result = await async_db_session.execute(text("SELECT version()"))
    assert result.scalar_one() is not None
