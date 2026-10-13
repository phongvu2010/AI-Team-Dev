"""Async Seed Data Runner for Local Development.

Discovers and executes all seed functions in `src/db/seeds/*_seed.py`.
Seed functions should be decorated with `@register_seed` or define an async `seed(session)` function.
"""

import asyncio
import importlib
import logging
import pkgutil
import sys
from collections.abc import Callable, Coroutine
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

# Ensure UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ensure 'src' is in sys.path automatically
_src_dir = Path(__file__).resolve().parent.parent.parent
if str(_src_dir) not in sys.path:
    sys.path.insert(0, str(_src_dir))

from db.session import AsyncSessionLocal  # noqa: E402

logger = logging.getLogger("db.seeds")

SeedFunction = Callable[[AsyncSession], Coroutine[Any, Any, None]]
_REGISTERED_SEEDS: list[tuple[str, SeedFunction]] = []


def register_seed(name: str | None = None) -> Callable[[SeedFunction], SeedFunction]:
    """Decorator to register a seed function with an optional friendly name."""

    def decorator(fn: SeedFunction) -> SeedFunction:
        seed_name = name or fn.__name__
        _REGISTERED_SEEDS.append((seed_name, fn))
        return fn

    return decorator


def auto_discover_seeds() -> None:
    """Discover all seed modules in db.seeds package."""
    import db.seeds as seeds_pkg

    package_path = seeds_pkg.__path__
    for _, module_name, is_pkg in pkgutil.iter_modules(package_path):
        if not is_pkg and (module_name.endswith("_seed") or module_name.startswith("seed_")):
            full_module_name = f"db.seeds.{module_name}"
            try:
                mod = importlib.import_module(full_module_name)
                # If module defines an async seed() function not already registered
                if hasattr(mod, "seed") and asyncio.iscoroutinefunction(mod.seed):
                    if not any(fn == mod.seed for _, fn in _REGISTERED_SEEDS):
                        _REGISTERED_SEEDS.append((module_name, mod.seed))
            except Exception as e:
                logger.error("Failed to import seed module %s: %s", full_module_name, e)


async def run_seeds() -> None:
    """Execute all discovered and registered seed functions sequentially."""
    auto_discover_seeds()

    if not _REGISTERED_SEEDS:
        logger.info("No seed functions discovered in src/db/seeds/.")
        return

    logger.info("Found %d seed functions to execute.", len(_REGISTERED_SEEDS))
    async with AsyncSessionLocal() as session:
        for seed_name, seed_fn in _REGISTERED_SEEDS:
            logger.info("🌱 Running seed: %s...", seed_name)
            try:
                await seed_fn(session)
                await session.commit()
                logger.info("✅ Seed '%s' completed successfully.", seed_name)
            except Exception as e:
                await session.rollback()
                logger.error("❌ Seed '%s' failed: %s", seed_name, e)
                raise


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    asyncio.run(run_seeds())
