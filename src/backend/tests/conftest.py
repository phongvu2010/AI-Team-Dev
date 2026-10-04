"""Pytest configuration and async test fixtures.

Provides dual-mode testing:
- Default: SQLite async in-memory fallback (:memory:) for isolated, rapid testing.
- PostgreSQL runtime: Supports live PostgreSQL / Supabase testing via TEST_DATABASE_URL.
- Cross-DB Edge Cases: Tests marked with @pytest.mark.postgres_only are automatically
  skipped when running against SQLite in-memory, preventing false failures on PG-specific types.
"""

import os
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from db.base import Base
from db.session import get_db_session

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:")


def is_postgres_test_db() -> bool:
    """Return True if TEST_DATABASE_URL points to a PostgreSQL database."""
    return "postgresql" in TEST_DATABASE_URL or "postgres" in TEST_DATABASE_URL


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip tests marked with `postgres_only` when executing against SQLite in-memory."""
    if not is_postgres_test_db():
        skip_pg = pytest.mark.skip(
            reason=(
                "Requires live PostgreSQL instance (e.g. pgvector, JSONB path, native enum). "
                "Set TEST_DATABASE_URL=postgresql+asyncpg://... to execute. Skipped on SQLite."
            )
        )
        for item in items:
            if "postgres_only" in item.keywords:
                item.add_marker(skip_pg)


_test_engine: AsyncEngine | None = None
_testing_session_local: async_sessionmaker[AsyncSession] | None = None


def get_test_engine() -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """Lazily initialize the async engine according to TEST_DATABASE_URL dialect."""
    global _test_engine, _testing_session_local
    if _test_engine is None:
        if is_postgres_test_db():
            connect_args: dict[str, int] = {}
            if (
                ":6543" in TEST_DATABASE_URL
                or "pooler.supabase.com" in TEST_DATABASE_URL
                or os.getenv("DB_DISABLE_STATEMENT_CACHE", "false").lower() == "true"
            ):
                connect_args["prepared_statement_cache_size"] = 0
                connect_args["statement_cache_size"] = 0

            _test_engine = create_async_engine(
                TEST_DATABASE_URL,
                pool_pre_ping=True,
                connect_args=connect_args,
            )
        else:
            try:
                import aiosqlite  # noqa: F401
            except ImportError:
                pytest.skip(
                    "aiosqlite is not installed. Run 'pip install aiosqlite' to enable async SQLite in-memory tests."
                )

            _test_engine = create_async_engine(
                TEST_DATABASE_URL,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )

        _testing_session_local = async_sessionmaker(
            bind=_test_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
    assert _testing_session_local is not None
    return _test_engine, _testing_session_local


@pytest.fixture(scope="session")
def db_dialect() -> str:
    """Return current test database dialect: 'postgresql' or 'sqlite'."""
    return "postgresql" if is_postgres_test_db() else "sqlite"


@pytest.fixture(scope="session", autouse=True)
def anyio_backend() -> str:
    """Set default backend for anyio/pytest-asyncio."""
    return "asyncio"


@pytest.fixture
async def async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Isolated async database session connected to in-memory SQLite."""
    engine, session_factory = get_test_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_client(
    request: pytest.FixtureRequest,
) -> AsyncGenerator[AsyncClient, None]:
    """HTTP async test client configured with FastAPI app.

    If the test also requests `async_db_session`, `get_db_session` is automatically
    overridden to that in-memory SQLite session.
    """
    if "async_db_session" in request.fixturenames:
        db_session = request.getfixturevalue("async_db_session")

        async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
            yield db_session

        app.dependency_overrides[get_db_session] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def client(
    async_db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    """HTTP async test client with `get_db_session` automatically overridden to in-memory SQLite.

    Use this fixture for testing API routes that inject `Depends(get_db_session)` to ensure
    all database interactions execute against the isolated in-memory SQLite database.
    """
    async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield async_db_session

    app.dependency_overrides[get_db_session] = _override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as test_client:
        yield test_client

    app.dependency_overrides.clear()
