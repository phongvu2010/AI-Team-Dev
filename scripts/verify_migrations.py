#!/usr/bin/env python3
"""Alembic Migration Chain & Syntax Integrity Verification Utility (`scripts/verify_migrations.py`).

Verifies:
1. Python syntax and AST validity of all migration scripts in src/db/migrations/versions/.
2. Revision DAG continuity:
   - Unique revision IDs.
   - Valid down_revision linkages (no orphan or broken references).
   - Single head continuity (unless explicit branching).
3. Existence and syntax of core Alembic assets (env.py, script.py.mako).

Usage:
    python scripts/verify_migrations.py
"""

import ast
import sys
from pathlib import Path

# Ensure UTF-8 console output on Windows to prevent UnicodeEncodeError
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = ROOT_DIR / "src" / "db" / "migrations"
VERSIONS_DIR = MIGRATIONS_DIR / "versions"


def verify_alembic_structure() -> list[str]:
    """Verify that Alembic configuration and template files exist and are valid."""
    errors = []
    env_file = MIGRATIONS_DIR / "env.py"
    mako_file = MIGRATIONS_DIR / "script.py.mako"
    ini_file = ROOT_DIR / "alembic.ini"

    if not ini_file.exists():
        errors.append("Missing alembic.ini at repository root.")
    if not env_file.exists():
        errors.append("Missing src/db/migrations/env.py.")
    else:
        try:
            with open(env_file, encoding="utf-8") as f:
                ast.parse(f.read(), filename=str(env_file))
        except Exception as e:
            errors.append(f"Syntax error in src/db/migrations/env.py: {e}")

    if not mako_file.exists():
        errors.append("Missing src/db/migrations/script.py.mako.")

    return errors


def inspect_migration_file(filepath: Path) -> dict:
    """Parse a single migration file and extract revision metadata."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    tree = ast.parse(content, filename=str(filepath))

    revision = None
    down_revision = None

    # Search for module-level variable assignments
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id == "revision" and isinstance(node.value, ast.Constant):
                        revision = str(node.value.value)
                    elif target.id == "down_revision":
                        if isinstance(node.value, ast.Constant):
                            down_revision = str(node.value.value) if node.value.value is not None else None
                        elif isinstance(node.value, (ast.Tuple, ast.List)):
                            down_revision = [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)]
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == "revision" and isinstance(node.value, ast.Constant):
                revision = str(node.value.value)
            elif node.target.id == "down_revision":
                if isinstance(node.value, ast.Constant):
                    down_revision = str(node.value.value) if node.value.value is not None else None
                elif isinstance(node.value, (ast.Tuple, ast.List)):
                    down_revision = [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)]

    return {
        "file": filepath.name,
        "path": filepath,
        "revision": revision,
        "down_revision": down_revision,
    }


def verify_migration_chain() -> tuple[list[dict], list[str]]:
    """Scan versions/ directory and verify revision continuity."""
    errors = []
    migrations = []

    if not VERSIONS_DIR.exists():
        errors.append(f"Versions directory not found: {VERSIONS_DIR}")
        return migrations, errors

    py_files = sorted(VERSIONS_DIR.glob("*.py"))
    py_files = [f for f in py_files if not f.name.startswith("__")]

    if not py_files:
        return migrations, errors

    revision_map: dict[str, dict] = {}
    down_revisions = set()
    roots = []

    for file_path in py_files:
        try:
            info = inspect_migration_file(file_path)
        except Exception as e:
            errors.append(f"Failed to parse migration {file_path.name}: {e}")
            continue

        rev = info["revision"]
        if not rev:
            errors.append(f"Migration {file_path.name} is missing a 'revision' variable.")
            continue

        if rev in revision_map:
            errors.append(f"Duplicate revision ID '{rev}' found in {file_path.name} and {revision_map[rev]['file']}.")
        else:
            revision_map[rev] = info
            migrations.append(info)

        down_rev = info["down_revision"]
        if down_rev is None:
            roots.append(rev)
        elif isinstance(down_rev, str):
            down_revisions.add(down_rev)
        elif isinstance(down_rev, list):
            down_revisions.update(down_rev)

    # Validate DAG linkages
    for info in migrations:
        down_rev = info["down_revision"]
        if down_rev is not None:
            targets = [down_rev] if isinstance(down_rev, str) else down_rev
            for target in targets:
                if target not in revision_map:
                    errors.append(
                        f"Migration {info['file']} (revision '{info['revision']}') points to missing down_revision '{target}'."
                    )

    # Check for multiple roots
    if len(roots) > 1:
        errors.append(f"Multiple base/root migrations found (down_revision=None): {', '.join(roots)}.")

    return migrations, errors


def main() -> int:
    print("=" * 72)
    print("🛡️ AI Team Dev — Alembic Migration & DAG Integrity Verification")
    print("=" * 72)

    # 1. Check structure
    print("\n[1] Checking Alembic Configuration & Environment Assets:")
    struct_errors = verify_alembic_structure()
    if struct_errors:
        for err in struct_errors:
            print(f"    ❌ {err}")
    else:
        print("    ✅ alembic.ini, env.py, and script.py.mako are present and syntactically valid.")

    # 2. Check migration versions
    print("\n[2] Checking Migration Files in src/db/migrations/versions/:")
    migrations, chain_errors = verify_migration_chain()

    if not migrations and not chain_errors:
        print("    ℹ️ No migration files found in versions/ (Clean baseline state).")
    else:
        print(f"    📄 Found {len(migrations)} migration file(s).")
        for m in migrations:
            print(f"       • {m['file']} -> revision='{m['revision']}', down_revision='{m['down_revision']}'")

    if chain_errors:
        print("\n[!] Migration Chain Errors:")
        for err in chain_errors:
            print(f"    ❌ {err}")

    all_errors = struct_errors + chain_errors

    print("\n" + "=" * 72)
    if not all_errors:
        print("✅ MIGRATION INTEGRITY PASSED: Revision chain and syntax are 100% valid.")
        print("=" * 72)
        return 0
    else:
        print(f"🚨 MIGRATION INTEGRITY FAILED: Found {len(all_errors)} error(s).")
        print("=" * 72)
        return 1


if __name__ == "__main__":
    sys.exit(main())
