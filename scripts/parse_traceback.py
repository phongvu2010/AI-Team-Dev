#!/usr/bin/env python3
"""Traceback Micro-Patcher & Defect Ticket Formatter for AI Team Dev (`scripts/parse_traceback.py`).

Parses raw error outputs from Pytest, Ruff, and Node test runners.
Extracts the exact target file, line range, failed assertion, and isolated code context
to produce token-optimized [MICRO-PATCH REQUIRED] tickets for Dev Agents.

Usage:
    python scripts/parse_traceback.py [error_log.txt]
    pytest ... | python scripts/parse_traceback.py
"""

import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def extract_pytest_defects(raw_text: str) -> list[dict]:
    """Extract individual test failures and file tracebacks from Pytest output."""
    defects = []
    
    # Split into failure blocks (Pytest separates failures with '___ test_name ___')
    failure_blocks = re.split(r"_{3,}\s+(.*?)\s+_{3,}", raw_text)
    
    if len(failure_blocks) > 1:
        for i in range(1, len(failure_blocks), 2):
            test_name = failure_blocks[i].strip()
            block_content = failure_blocks[i + 1] if i + 1 < len(failure_blocks) else ""
            
            # Find all File "...", line X entries
            file_matches = list(re.finditer(r'File "([^"]+)", line (\d+)(?:, in (\w+))?', block_content))
            if not file_matches:
                # Alternative syntax: path/file.py:line: in test_name
                file_matches = list(re.finditer(r'([a-zA-Z0-9_\-\./\\]+\.py):(\d+):', block_content))
            
            target_file = None
            target_line = None
            func_name = test_name
            
            # Find the most relevant file in src/ (exclude test runner internal libraries)
            for m in reversed(file_matches):
                fpath = m.group(1)
                if "site-packages" not in fpath and ("src/" in fpath or not fpath.startswith("/")):
                    target_file = fpath
                    target_line = int(m.group(2))
                    if len(m.groups()) >= 3 and m.group(3):
                        func_name = m.group(3)
                    break
            
            # If no src/ file found, take the last one
            if not target_file and file_matches:
                target_file = file_matches[-1].group(1)
                target_line = int(file_matches[-1].group(2))
            
            # Extract assertion or exception lines (lines starting with 'E   ')
            error_lines = [line[4:].strip() for line in block_content.splitlines() if line.startswith("E   ")]
            error_msg = "\n".join(error_lines) if error_lines else "Assertion / Runtime Error"
            
            if target_file and target_line:
                defects.append({
                    "test_name": test_name,
                    "file_path": target_file,
                    "line": target_line,
                    "function": func_name,
                    "error_message": error_msg,
                })
    else:
        # Fallback regex search across entire text
        pattern = r'File "([^"]+)", line (\d+)(?:, in (\w+))?[\s\S]*?(?:E\s+([^\n]+)|Exception: ([^\n]+)|Error: ([^\n]+))'
        for m in re.finditer(pattern, raw_text):
            fpath = m.group(1)
            line_no = int(m.group(2))
            func = m.group(3) or "unknown"
            err = m.group(4) or m.group(5) or m.group(6) or "Exception occurred"
            defects.append({
                "test_name": func,
                "file_path": fpath,
                "line": line_no,
                "function": func,
                "error_message": err.strip(),
            })

    return defects


def get_code_context(file_path: str, line_no: int, window: int = 5) -> tuple[int, int, str]:
    """Retrieve surrounding lines of code around the error line."""
    p = Path(file_path)
    if not p.is_absolute():
        p = ROOT_DIR / p
    
    if not p.exists() or not p.is_file():
        return line_no, line_no, ""
    
    try:
        lines = p.read_text(encoding="utf-8").splitlines()
        start_line = max(1, line_no - window)
        end_line = min(len(lines), line_no + window)
        
        snippet = []
        for i in range(start_line, end_line + 1):
            marker = ">> " if i == line_no else "   "
            snippet.append(f"{marker}{i:4d} | {lines[i - 1]}")
        
        return start_line, end_line, "\n".join(snippet)
    except Exception:
        return line_no, line_no, ""


def format_micro_patch_ticket(defect: dict, index: int = 1) -> str:
    """Format a single defect into a structured [MICRO-PATCH REQUIRED] action ticket."""
    fpath = defect["file_path"]
    line_no = defect["line"]
    start_line, end_line, snippet = get_code_context(fpath, line_no)
    
    # Determine responsible dev squad based on path
    target_squad = "backend-dev"
    if "src/db/" in fpath:
        target_squad = "db-dev"
    elif "src/frontend/" in fpath or "src/mobile/" in fpath:
        target_squad = "frontend-dev"
    
    ticket = f"""
================================================================================
🚨 [MICRO-PATCH REQUIRED #{index}] -> Assignee: `{target_squad}`
================================================================================
- **Mục tiêu**: Khắc phục lỗi kiểm thử tại `{defect['test_name']}`
- **Tập tin bị lỗi**: `{fpath}#L{line_no}` (Khoảng can thiệp: L{start_line}-L{end_line})
- **Chi tiết lỗi**: {defect['error_message']}

🔍 ĐOẠN MÃ NGUỒN CẦN SỬA (Context Snippet):
```python
{snippet}
```

⚡ CHỈ DẪN SỬA ĐỔI CHO AGENT (MICRO-PATCH GUARDRAILS):
1. TUYỆT ĐỐI KHÔNG viết lại toàn bộ file. Chỉ sử dụng công cụ `replace_file_content` sửa chính xác 1-5 dòng code bị lỗi tại vị trí dòng {line_no}.
2. Giữ nguyên toàn bộ docstring, comments và các hàm xung quanh.
3. Báo cáo lại kết quả với cờ `[FIX-COMPLETED]` và `Contract Modified: TRUE/FALSE`.
================================================================================
"""
    return ticket


def main():
    if len(sys.argv) > 1 and sys.argv[1] not in ("-", "--help"):
        input_file = Path(sys.argv[1])
        if not input_file.exists():
            print(f"❌ File not found: {input_file}", file=sys.stderr)
            sys.exit(1)
        raw_text = input_file.read_text(encoding="utf-8")
    else:
        raw_text = sys.stdin.read()

    if not raw_text.strip():
        print("ℹ️ No traceback input provided.")
        sys.exit(0)

    defects = extract_pytest_defects(raw_text)
    
    if not defects:
        print("✔ Không phát hiện traceback lỗi nào trong log đầu vào.")
        sys.exit(0)

    print(f"\n🔍 Phát hiện {len(defects)} vị trí lỗi cần áp dụng Micro-Patch:\n")
    for idx, defect in enumerate(defects, start=1):
        print(format_micro_patch_ticket(defect, index=idx))


if __name__ == "__main__":
    main()
