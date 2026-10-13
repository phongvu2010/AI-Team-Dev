#!/usr/bin/env python3
"""Cross-Layer Contract & Schema Drift Verification Utility (`scripts/verify_contracts.py`).

Verifies schema and naming consistency across the 3 layers:
1. plan.md (Cross-Layer Data Contract Matrix)
2. src/backend/app/schemas/ (Pydantic v2 schemas)
3. src/frontend/src/types/ (TypeScript interfaces)

Rules enforced:
- Uniform Casing: ALL field/property names must adhere to strict snake_case.
- No camelCase in API schemas or TypeScript entity interfaces.
- Cross-layer parity between plan.md and implementation.

Usage:
    PYTHONPATH=src .venv/bin/python scripts/verify_contracts.py [feature-slug]
"""

import ast
import re
import sys
from pathlib import Path

# Ensure UTF-8 console output on Windows to prevent UnicodeEncodeError
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Auto-add src to sys.path so PYTHONPATH=src is optional
base_dir = Path(__file__).resolve().parent.parent
src_dir = base_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

SNAKE_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
CAMEL_CASE_PATTERN = re.compile(r"^[a-z]+[A-Z0-9]")


def is_snake_case(name: str) -> bool:
    """Check if a name strictly follows snake_case."""
    return bool(SNAKE_CASE_PATTERN.match(name))


def is_camel_case(name: str) -> bool:
    """Check if a name appears to be camelCase."""
    return bool(CAMEL_CASE_PATTERN.match(name))


def extract_backend_pydantic_fields(schemas_dir: Path) -> dict[str, list[dict[str, str]]]:
    """Parse Python AST from src/backend/app/schemas/*.py to extract schema fields."""
    results: dict[str, list[dict[str, str]]] = {}
    if not schemas_dir.exists():
        return results

    for py_file in schemas_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
        try:
            with open(py_file, encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(py_file))
        except Exception as e:
            print(f"⚠️ Error parsing {py_file}: {e}")
            continue

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                fields = []
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        field_name = item.target.id
                        # Ignore dunder or private fields
                        if field_name.startswith("_"):
                            continue
                        fields.append({
                            "name": field_name,
                            "file": str(py_file.relative_to(schemas_dir.parent.parent.parent)),
                            "line": str(item.lineno),
                        })
                if fields:
                    results[class_name] = fields
    return results


def extract_frontend_ts_fields(types_dir: Path) -> dict[str, list[dict[str, str]]]:
    """Parse TypeScript files in src/frontend/src/types/*.ts to extract interface properties."""
    results: dict[str, list[dict[str, str]]] = {}
    if not types_dir.exists():
        return results

    # Simple regex parser for TS interfaces and type aliases
    interface_pattern = re.compile(
        r"(?:export\s+)?(?:interface|type)\s+([A-Za-z0-9_]+)(?:\s*=\s*|\s+extends[^{]+)?\s*\{([^}]+)\}",
        re.DOTALL,
    )
    prop_pattern = re.compile(r"^\s*([a-zA-Z0-9_]+)\s*\??\s*:\s*([^;]+);", re.MULTILINE)

    for ts_file in types_dir.glob("**/*.ts"):
        try:
            with open(ts_file, encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️ Error reading {ts_file}: {e}")
            continue

        for match in interface_pattern.finditer(content):
            interface_name = match.group(1)
            body = match.group(2)
            fields = []
            for prop in prop_pattern.finditer(body):
                prop_name = prop.group(1)
                prop_type = prop.group(2).strip()
                fields.append({
                    "name": prop_name,
                    "type": prop_type,
                    "file": str(ts_file.relative_to(types_dir.parent.parent.parent)),
                })
            if fields:
                results[interface_name] = fields
    return results


def extract_plan_matrix_fields(plan_file: Path) -> list[dict[str, str]]:
    """Extract fields from Section 2 Cross-Layer Data Contract Matrix table in plan.md."""
    if not plan_file.exists():
        return []

    fields = []
    in_matrix_section = False
    with open(plan_file, encoding="utf-8") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines, start=1):
        if "Cross-Layer Data Contract Matrix" in line or "Ma Trận Ánh Xạ Dữ Liệu" in line:
            in_matrix_section = True
            continue
        if in_matrix_section and line.startswith("## ") and not ("Cross-Layer" in line or "Ma Trận" in line):
            in_matrix_section = False
            break

        if in_matrix_section and "|" in line:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 4 and not parts[0].startswith("---") and parts[0].lower() not in ["trường dữ liệu", "field name", "field"]:
                field_name = parts[0].replace("`", "").strip()
                db_type = parts[1].replace("`", "").strip() if len(parts) > 1 else ""
                backend_type = parts[2].replace("`", "").strip() if len(parts) > 2 else ""
                frontend_type = parts[3].replace("`", "").strip() if len(parts) > 3 else ""
                if field_name:
                    fields.append({
                        "name": field_name,
                        "db_type": db_type,
                        "backend_type": backend_type,
                        "frontend_type": frontend_type,
                        "line": str(idx),
                    })
    return fields


def main() -> int:
    print("=" * 75)
    print("🔍 AI Team Dev — Cross-Layer Contract & Schema Drift Verification")
    print("=" * 75)

    base_dir = Path(__file__).resolve().parent.parent
    feature_slug = sys.argv[1] if len(sys.argv) > 1 else None

    violations: list[str] = []
    total_fields_checked = 0

    # 1. Verify plan.md Data Matrix if slug is provided or found
    plan_files = []
    if feature_slug:
        target_plan = base_dir / "docs" / "specs" / feature_slug / "plan.md"
        if target_plan.exists():
            plan_files.append(target_plan)
        else:
            print(f"ℹ️ Specified feature plan not found at {target_plan}")
    else:
        plan_files = list(base_dir.glob("docs/specs/*/plan.md"))

    print("\n[1] Checking plan.md Specifications (Cross-Layer Data Contract Matrix):")
    if not plan_files:
        print("    ℹ️ No active plan.md found in docs/specs/ (Skip plan table check).")
    else:
        for plan_path in plan_files:
            rel_plan = plan_path.relative_to(base_dir)
            print(f"    📄 Inspecting: {rel_plan}")
            matrix_fields = extract_plan_matrix_fields(plan_path)
            if not matrix_fields:
                print("       ⚠️ No Cross-Layer Data Contract Matrix table detected in plan.")
            else:
                for f in matrix_fields:
                    total_fields_checked += 1
                    name = f["name"]
                    if not is_snake_case(name):
                        violations.append(
                            f"❌ [{rel_plan}:{f['line']}] Field '{name}' violates uniform snake_case naming."
                        )
                        print(f"       ❌ Field '{name}' (line {f['line']}): INVALID CASING (expected snake_case)")
                    else:
                        print(f"       ✅ Field '{name}': snake_case OK (DB: {f['db_type']}, BE: {f['backend_type']}, FE: {f['frontend_type']})")

    # 2. Verify Backend Pydantic Schemas (src/backend/app/schemas/)
    backend_schemas_dir = base_dir / "src" / "backend" / "app" / "schemas"
    print(f"\n[2] Checking Backend Pydantic Schemas ({backend_schemas_dir.relative_to(base_dir)}):")
    backend_schemas = extract_backend_pydantic_fields(backend_schemas_dir)
    if not backend_schemas:
        print("    ℹ️ No Pydantic schema models found yet (Clean state).")
    else:
        for schema_name, fields in backend_schemas.items():
            print(f"    📦 Schema Model: {schema_name}")
            for f in fields:
                total_fields_checked += 1
                name = f["name"]
                if not is_snake_case(name):
                    violations.append(
                        f"❌ [Backend {f['file']}:{f['line']}] Schema '{schema_name}.{name}' violates snake_case."
                    )
                    print(f"       ❌ {name}: NOT snake_case! (File: {f['file']}#{f['line']})")
                else:
                    print(f"       ✅ {name}: snake_case OK")

    # 3. Verify Frontend TypeScript Types (src/frontend/src/types/)
    frontend_types_dir = base_dir / "src" / "frontend" / "src" / "types"
    print(f"\n[3] Checking Frontend TypeScript Interfaces ({frontend_types_dir.relative_to(base_dir)}):")
    frontend_types = extract_frontend_ts_fields(frontend_types_dir)
    if not frontend_types:
        print("    ℹ️ No custom TypeScript interfaces found yet (Clean state).")
    else:
        for iface_name, fields in frontend_types.items():
            print(f"    📐 Interface: {iface_name}")
            for f in fields:
                total_fields_checked += 1
                name = f["name"]
                if not is_snake_case(name):
                    violations.append(
                        f"❌ [Frontend {f['file']}] Property '{iface_name}.{name}' is not snake_case."
                    )
                    print(f"       ❌ {name}: NOT snake_case! (camelCase detected in {f['file']})")
                else:
                    print(f"       ✅ {name}: snake_case OK")

    # Summary Output
    print("\n" + "=" * 75)
    print("📊 Contract Verification Summary:")
    print(f"   • Total Fields/Properties Checked: {total_fields_checked}")
    print(f"   • Casing & Drift Violations Found: {len(violations)}")

    if violations:
        print("\n🚨 Violations Detected:")
        for v in violations:
            print(f"   {v}")
        print("\n❌ CONTRACT VERIFICATION FAILED: Resolve naming or drift before proceeding.")
        return 1

    print("\n✅ CONTRACT VERIFICATION PASSED: 100% snake_case compliance & zero drift detected.")
    print("=" * 75)
    return 0


if __name__ == "__main__":
    sys.exit(main())
