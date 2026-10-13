#!/usr/bin/env python3
"""Offline Alembic Migration Generator.

Generates a standard, valid Alembic migration template in src/db/migrations/versions/
without requiring an active PostgreSQL database connection.

Usage:
    PYTHONPATH=src .venv/bin/python src/db/migrations/generate_offline_migration.py <slug_name>
"""

import datetime
import glob
import os
import re
import sys
import uuid
from pathlib import Path

# Ensure UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ensure 'src' is in sys.path automatically
_src_dir = Path(__file__).resolve().parent.parent.parent
if str(_src_dir) not in sys.path:
    sys.path.insert(0, str(_src_dir))

VERSIONS_DIR = os.path.join(os.path.dirname(__file__), "versions")


def get_latest_revision() -> str | None:
    """Finds the most recent revision ID by scanning versions/ directory."""
    migration_files = glob.glob(os.path.join(VERSIONS_DIR, "*.py"))
    revisions = []

    for filepath in migration_files:
        filename = os.path.basename(filepath)
        if filename.startswith("__"):
            continue
        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
                rev_match = re.search(r"^revision:\s*str\s*=\s*['\"]([^'\"]+)['\"]", content, re.M)
                if rev_match:
                    revisions.append((os.path.getmtime(filepath), rev_match.group(1)))
        except OSError:
            continue

    if not revisions:
        return None
    # Sort by file modification time to find latest
    revisions.sort(key=lambda x: x[0])
    return revisions[-1][1]


def create_migration(slug: str) -> str:
    """Creates a new migration file with deterministic revision ID and down_revision."""
    os.makedirs(VERSIONS_DIR, exist_ok=True)
    slug_clean = re.sub(r"[^a-zA-Z0-9_]+", "_", slug.strip().lower())

    # Generate 12-char hex revision ID (standard Alembic format)
    rev_id = uuid.uuid4().hex[:12]
    down_rev = get_latest_revision()
    now_str = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S.000000")

    filename = f"{rev_id}_{slug_clean}.py"
    target_path = os.path.join(VERSIONS_DIR, filename)

    down_rev_repr = f"'{down_rev}'" if down_rev else "None"

    template = f'''"""{slug_clean}

Revision ID: {rev_id}
Revises: {down_rev or "None"}
Create Date: {now_str}
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Uuid

# revision identifiers, used by Alembic.
revision: str = "{rev_id}"
down_revision: Union[str, None] = {down_rev_repr}
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # TODO (db-dev): Add table creation and indexes matching src/db/models/
    # Example:
    # op.create_table(
    #     "{slug_clean}",
    #     sa.Column("id", Uuid, primary_key=True),
    #     sa.Column("title", sa.String(255), nullable=False),
    #     sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    #     sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    # )
    # op.create_index(op.f("ix_{slug_clean}_title"), "{slug_clean}", ["title"], unique=False)
    pass


def downgrade() -> None:
    # TODO (db-dev): Add reverse operations
    # Example:
    # op.drop_index(op.f("ix_{slug_clean}_title"), table_name="{slug_clean}")
    # op.drop_table("{slug_clean}")
    pass
'''

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(template)

    return target_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: PYTHONPATH=src python src/db/migrations/generate_offline_migration.py <slug_name>")
        sys.exit(1)

    slug_arg = sys.argv[1]
    created_file = create_migration(slug_arg)
    print(f"✓ Offline Alembic migration generated at: {created_file}")
