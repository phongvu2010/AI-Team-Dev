---
feature_slug: "<feature-slug>"
version: "1.0.0"
artifact_type: "review-report"
reviewer: "code-reviewer"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
verdict: "APPROVED" # APPROVED | CHANGES_REQUESTED
iteration: 1 # Vòng lặp review (1 -> 3)
findings_summary:
  critical: 0
  major: 0
  minor: 0
  nit: 0
---

# Principal Code Review & Security Audit Report: `<Feature Name>`

> **Báo cáo Thẩm định Kiến trúc & Bảo mật Độc lập**: Đánh giá toàn diện các thay đổi mã nguồn mới trong `src/` qua phân tích `git diff`, đối chiếu trực tiếp với `plan.md` và `test-report.md`.

---

## 1. Bảng Điểm Thẩm Định Cổng Chất Lượng (Quality Gate Scorecard)

| Hạng mục Kiểm định | Tiêu Chuẩn Thẩm Định | Kết quả | Đánh giá Chi tiết |
| :--- | :--- | :---: | :--- |
| **1. Tuân thủ Hợp đồng (Contract Alignment)** | Khớp 100% Ma trận dữ liệu xuyên tầng trong `plan.md` | PASS | Tên trường, kiểu dữ liệu, casing `snake_case` đồng bộ. |
| **2. Database & Hiệu năng (`src/db/`)** | Không N+1 query (`selectinload`), đủ index, migration an toàn | PASS | Đã tối ưu eager loading, đánh index cho khóa ngoại. |
| **3. Backend & Bảo mật (`src/backend/`)** | Pydantic v2 validation giới hạn độ dài, quản lý transaction | PASS | Không lộ secret, kiểm tra chặt chẽ payload đầu vào. |
| **4. Frontend & Trải nghiệm (`src/frontend/`)** | Strict TypeScript (0 `any`), đủ 4 trạng thái UI, chuẩn A11y | PASS | Khai báo types chuẩn, có skeleton, retry, CTA đầy đủ. |
| **5. Toàn vẹn Kiểm thử (`test-report.md`)** | 100% test cases PASSED, không bỏ sót kịch bản lỗi | PASS | Kiểm thử đạt độ phủ theo đúng Acceptance Criteria. |

---

## 2. Phạm Vi Mã Nguồn Được Audit (Git Diff Scope)

```text
# Git Status & Diff Summary:
src/db/...                |  +X -Y
src/backend/...           |  +X -Y
src/frontend/...          |  +X -Y
X files changed, Y insertions(+), Z deletions(-)
```

---

## 3. Danh Sách Phát Hiện Chi Tiết (Structured Finding Tickets)

> 💡 Phân loại mức độ nghiêm trọng:
> - `[CRITICAL]`: Lỗ hổng bảo mật nghiêm trọng, nguy cơ mất dữ liệu, crash hệ thống hoặc phá vỡ Hợp đồng API Contract (Bắt buộc sửa trước khi merge).
> - `[MAJOR]`: Lỗi N+1 query tiềm ẩn, thiếu transaction rollback, dùng ép kiểu `any` trong TypeScript, thiếu validation giới hạn độ dài (Bắt buộc sửa).
> - `[MINOR]`: Code smell, cú pháp chưa tối ưu, thiếu comment giải thích logic phức tạp (Khuyến nghị sửa).
> - `[NIT]`: Đề xuất cải thiện phong cách code hoặc đặt tên biến rõ ràng hơn (Tùy chọn).

### [REV-01] `<Tiêu đề phát hiện ngắn gọn>`
- **Mã Phát hiện**: `REV-01`
- **Mức độ (Severity)**: `CRITICAL` | `MAJOR` | `MINOR` | `NIT`
- **Phân loại (Category)**: `Contract Alignment` | `Security / OWASP` | `Performance & N+1` | `Type Safety` | `A11y & UX`
- **Tác tử Phụ trách (Target Agent)**: `db-dev` (`src/db/`) | `backend-dev` (`src/backend/`) | `frontend-dev` (`src/frontend/`)
- **Vị trí Phát hiện (Target File & Line)**: `src/.../file.ts#L...`
- **Đoạn Code Vi phạm (Diff Evidence)**:
  ```typescript
  // Trích xuất đoạn code chưa chuẩn
  ```
- **Lý do Vi phạm (Violation Rationale)**:
  - ...
- **Hướng dẫn Khắc phục (Actionable Remediation)**:
  - ...

---

## 4. Kết Luận Nghiệm Thu & Đóng Gói (Sign-off & Next Steps)

- **Quyết định Cuối cùng (Final Verdict)**: `APPROVED` | `CHANGES_REQUESTED`

### Trường hợp 1: Khi Verdict = `CHANGES_REQUESTED`
- Yêu cầu Tech Lead Orchestrator kích hoạt **Giao thức Thông điệp [REVIEW-FIX ACTION REQUIRED]** gửi tới các tác tử phụ trách nêu tại Mục 3.
- Sau khi Dev Squad sửa xong, `qa-tester` chạy lại bài test và `code-reviewer` thẩm định lại lần 2 (tối đa 3 vòng lặp).

### Trường hợp 2: Khi Verdict = `APPROVED`
Mã nguồn đã sẵn sàng 100% để đóng gói. Đề xuất lệnh Git Commit chuẩn Conventional Commits cho Tech Lead Orchestrator tại Bước 5:

```bash
git add src/ docs/specs/<feature-slug>/
git add pyproject.toml src/frontend/package*.json 2>/dev/null || true
git commit -m "feat(<feature-slug>): implement <tên tính năng ngắn gọn>

- DB: add SQLAlchemy 2.0 models & migrations in src/db/
- Backend: implement FastAPI schemas, services & endpoints in src/backend/
- Frontend: build Next.js UI components & typed API client in src/frontend/
- Quality: 100% automated tests passed, code review approved
- Specs: docs/specs/<feature-slug>/plan.md"
```
