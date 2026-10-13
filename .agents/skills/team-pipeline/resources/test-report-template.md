---
feature_slug: "<feature-slug>"
version: "1.0.0"
artifact_type: "test-report"
tester: "qa-tester"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
overall_status: "PASSED" # PASSED | FAILED
iteration: 1 # Vòng lặp kiểm thử (1 -> 3)
metrics:
  total_tests: 0
  passed: 0
  failed: 0
  skipped: 0
  duration_seconds: 0.0
---

# QA & Automated Test Report: `<Feature Name>`

> **Báo cáo Kiểm thử Tự động**: Tài liệu đánh giá chất lượng toàn diện độc lập cho tính năng `<Feature Name>`, bao gồm linter, unit/integration test backend/DB và typecheck frontend.

---

## 1. Tóm Tắt & Chỉ Số Kiểm Thử (Executive Summary & Metrics)

- **Trạng thái Tổng thể**: `PASSED` | `FAILED`
- **Vòng lặp Kiểm thử (Iteration)**: `<iteration_number> / 3`
- **Tỷ lệ Vượt qua (Pass Rate)**: `100%`

| Hạng mục Kiểm định | Công cụ (Runner) | Phạm vi | Kết quả | Passed | Failed | Thời gian |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **Linter & Code Style** | `.venv/bin/ruff check src/` | Toàn bộ `src/` | PASSED | - | 0 | 0.05s |
| **Database Layer** | `PYTHONPATH=src .venv/bin/pytest` | `src/backend/tests/` | PASSED | 0 | 0 | 0.02s |
| **Backend API Endpoints** | `PYTHONPATH=src .venv/bin/pytest` | `src/backend/tests/` | PASSED | 0 | 0 | 0.03s |
| **Frontend TypeScript Safety**| `npm --prefix src/frontend run typecheck` | `src/frontend/` | PASSED | - | 0 | 1.20s |

---

## 2. Ma Trận Đối Chiếu Kịch Bản Kiểm Thử (Acceptance Criteria vs Results)

| Mã AC (`plan.md`) | Mã Test Case | Tên Hàm / Kịch Bản Kiểm Thử | Tầng Phụ Trách | Kết Quả | Ghi Chú |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **AC-01** | `TC-01` | `test_create_resource_success` | Backend API | ✅ PASSED | Trả về 201 Created |
| **AC-02** | `TC-02` | `test_create_resource_validation_error` | Backend API | ✅ PASSED | Trả về 422 Unprocessable |
| **AC-03** | `TC-03` | `test_unique_constraint_enforcement` | Database / API | ✅ PASSED | Ràng buộc hoạt động |
| **AC-04** | `TC-04` | `UI States (Loading, Error, Empty, Success)` | Frontend Web | ✅ PASSED | Render 4 trạng thái |
| **AC-05** | `TC-05` | `TypeScript Strict Safety Check` | Frontend | ✅ PASSED | 0 type errors, 0 any |

---

## 3. Lệnh Thực Thi & Nhật Ký Đầu Ra (Execution Logs)

```text
# 1. Ruff Linter Output:
.venv/bin/ruff check src/
All checks passed!

# 2. Pytest Output:
PYTHONPATH=src ./.venv/bin/pytest src/backend/tests -v
...
=== X passed in Y.YYs ===

# 3. Frontend Typecheck Output:
npm --prefix src/frontend run typecheck
...
```

---

## 4. Phiếu Báo Lỗi Chi Tiết (Structured Bug Tickets — Dành cho Self-Healing)

> 💡 Nếu toàn bộ bài test đều `PASSED`, ghi: *"Không phát hiện lỗi. Hệ thống đạt 100% tiêu chí nghiệm thu kiểm thử."*

### [BUG-01] `<Tiêu đề lỗi ngắn gọn>`
- **Mã Lỗi**: `BUG-01`
- **Mức độ (Severity)**: `CRITICAL` | `MAJOR` | `MINOR`
- **Tác tử Chịu trách nhiệm (Target Agent)**: `db-dev` (`src/db/`) | `backend-dev` (`src/backend/`) | `frontend-dev` (`src/frontend/`)
- **Vị trí Phát hiện (Target File & Line)**: `src/.../file.py#L...`
- **Mã Kịch bản Thất bại (Failed Test ID)**: `TC-01` (`test_function_name`)
- **Nhật ký Lỗi & Traceback (Diagnostics)**:
  ```text
  <dán chính xác đoạn log traceback hoặc error message>
  ```
- **Phân tích Nguyên nhân Gốc (Root Cause Analysis)**:
  - ...
- **Các bước Tái hiện (Reproduction Command)**:
  ```bash
  PYTHONPATH=src .venv/bin/pytest src/backend/tests/test_file.py -k "test_function_name"
  ```
- **Đề xuất Khắc phục (Recommended Fix)**:
  - ...
- **Trạng thái Xử lý (Status)**: `OPEN` # OPEN | IN_PROGRESS | RESOLVED | RE-TESTED

---

## 5. Kết Luận Nghiệm Thu Kiểm Thử (QA Sign-off)

- [ ] **Đủ điều kiện chuyển sang Giai đoạn 4 (`code-reviewer`)**: Có (khi `overall_status: PASSED` 100%).
- [ ] **Yêu cầu kích hoạt Vòng lặp Tự sửa lỗi (Self-Healing Loop)**: Có (khi có ít nhất 1 bài test thất bại).
