---
feature_slug: "<feature-slug>"
version: "1.0.0"
artifact_type: "plan"
author: "planner"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
status: "READY_FOR_DEV" # DRAFT | READY_FOR_DEV | IN_DEV | TESTING | REVIEWING | COMPLETED
iteration: 1
---

# Technical Specification & Execution Plan: `<Feature Name>`

> **Tài liệu Single Source of Truth (SSOT)**: Bản đặc tả kỹ thuật và hợp đồng giao tiếp giữa các tầng cho tính năng `<Feature Name>`. Mọi dev squad (`db-dev`, `backend-dev`, `frontend-dev`) và tester/reviewer (`qa-tester`, `code-reviewer`) bắt buộc tuân thủ hợp đồng này.

---

## 1. Tổng quan & Mục tiêu Nghiệp vụ (Overview & Objectives)
- **Tài liệu tham chiếu PRD**: [`docs/specs/<feature-slug>/prd.md`](./prd.md) (Biên soạn bởi `ba`, Status: `APPROVED_BY_USER`)
- **Mô tả tính năng**: ...
- **Mục tiêu cốt lõi**: ...
- **Phân định phạm vi**:
  - **Trong phạm vi (P0 - MVP)**: ...
  - **Giai đoạn tiếp theo (P1/P2 - Out of scope)**: ...
- **User Stories chính**:
  1. Là một `<vai_trò>`, tôi muốn `<hành_động>` để `<giá_trị_nhận_được>`.

---

## 2. Hợp Đồng Dữ Liệu Xuyên Tầng (Cross-Layer Data Contract Matrix)

> ⚠️ **Quy chuẩn Bắt buộc**:
> - **Casing chuẩn**: Toàn bộ payload JSON của REST API thống nhất sử dụng chuẩn `snake_case` (khớp 1:1 với tên thuộc tính Backend và Frontend interfaces).
> - **UUID**: Sinh tại tầng Python (`default=uuid.uuid4`), serialize sang client dưới dạng chuỗi RFC 4122 (`str` / `string`).
> - **Thời gian (Timestamps)**: Định dạng ISO 8601 UTC có timezone (ví dụ `2026-10-02T12:00:00Z`).
> - **Mảng dữ liệu**: Tầng DB dùng `JSON` chuẩn (kèm variant PG nếu cần), Backend dùng `list[T]`, Frontend dùng `T[]`.

| Trường Dữ Liệu | Kiểu DB (`SQLAlchemy / PG`) | Kiểu Backend (`Pydantic v2`) | Kiểu Frontend (`TypeScript`) | Nullable | Giá trị mặc định | Ràng buộc & Ghi chú |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| `id` | `Uuid` (Python `uuid.uuid4`) | `UUID` / `str` | `string` | Không | `uuid.uuid4` | Khóa chính PK, UUID v4 |
| `<field_name>` | `<SQLAlchemy Type>` | `<Pydantic Type & Validation>` | `<TypeScript Type>` | Có/Không | `None` / `...` | Giới hạn độ dài, Regex |
| `created_at` | `DateTime(timezone=True)` | `datetime` | `string` | Không | `func.now()` | ISO 8601 UTC string |
| `updated_at` | `DateTime(timezone=True)` | `datetime` | `string` | Không | `func.now()` | Tự động cập nhật onupdate |

---

## 3. Data Contract — Thiết kế Database (`db-dev` — Đích: `src/db/`)

### 3.1. Bảng & SQLAlchemy 2.0 Models (`src/db/models/<module>.py`)
- **Tên bảng (`__tablename__`)**: `<table_name>`
- **Kế thừa bắt buộc**: `Base`, `UUIDPrimaryKeyMixin` (hoặc `TimestampMixin`) từ `src/db/base.py`.
- **Ràng buộc & Chỉ mục**:
  - `UniqueConstraint`: ...
  - `Index`: Đánh chỉ mục cho các trường thường xuyên `WHERE`, `ORDER BY`, `JOIN`.
- **Đảm bảo Cross-DB Test**:
  - UUID khóa chính: `Uuid(as_uuid=True)` kèm `default=uuid.uuid4`.
  - Mảng dữ liệu: `JSON` với `default=list`.

### 3.2. Relationships & Repositories (`src/db/repositories/<module>.py`)
- **Quan hệ**: Chỉ định rõ `relationship(...)`.
- **Chiến lược Eager Loading chống N+1**: Sử dụng `selectinload` hoặc `joinedload` trong các hàm truy vấn.
- **Hàm Repository cung cấp cho Backend**:
  ```python
  async def get_<resource>_by_id(session: AsyncSession, id: UUID) -> <Model> | None: ...
  async def list_<resource>s(session: AsyncSession, skip: int, limit: int) -> list[<Model>]: ...
  async def create_<resource>(session: AsyncSession, data: dict) -> <Model>: ...
  ```

### 3.3. Kịch bản Dữ liệu Mẫu Ban đầu (Seed Data — `src/db/seeds/<module>_seed.py`)
- Dữ liệu khởi tạo (Admin, cấu hình mặc định, sample items).
- Đảm bảo tính **Idempotent** (kiểm tra tồn tại trước khi insert).

---

## 4. API Contract — Đặc tả REST API (`backend-dev` & `frontend-dev`)

### 4.1. Danh mục Endpoints

| Method | Path | Quyền / Auth | Request Schema | Response Schema | Status Code |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/<resource>` | Public / Bearer | Query params | `<Resource>ListResponse` | `200 OK` |
| `POST` | `/api/v1/<resource>` | Bearer | `<Resource>Create` | `<Resource>Response` | `201 Created` |
| `GET` | `/api/v1/<resource>/{id}` | Public / Bearer | Không | `<Resource>Response` | `200 OK` |
| `PUT/PATCH` | `/api/v1/<resource>/{id}` | Bearer | `<Resource>Update` | `<Resource>Response` | `200 OK` |
| `DELETE` | `/api/v1/<resource>/{id}` | Bearer | Không | Không | `204 No Content` |

### 4.2. Chi tiết Request / Response Schemas

#### Endpoint: `POST /api/v1/<resource>`
- **Request Body JSON**:
  ```json
  {
    "title": "string (bắt buộc, max 255 ký tự)",
    "description": "string | null (tối đa 2000 ký tự)"
  }
  ```
- **Response Success `201 Created`**:
  ```json
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Tên item",
    "description": "Mô tả chi tiết",
    "created_at": "2026-10-02T12:00:00Z",
    "updated_at": "2026-10-02T12:00:00Z"
  }
  ```
- **Chuẩn hóa Error Responses**:
  - `400 Bad Request`: `{"detail": "Mô tả vi phạm nghiệp vụ"}`
  - `401 Unauthorized`: `{"detail": "Chưa xác thực hoặc token hết hạn"}`
  - `404 Not Found`: `{"detail": "Không tìm thấy tài nguyên yêu cầu"}`
  - `409 Conflict`: `{"detail": "Dữ liệu đã tồn tại hoặc xung đột khóa unique"}`
  - `422 Unprocessable Entity`: Cấu trúc lỗi chuẩn validation của FastAPI/Pydantic v2.

### 4.3. Wave 1 Mock Fixture (`src/frontend/src/lib/api/mocks/<resource>.ts`)
```typescript
import { <Resource> } from "@/types/<resource>";

export const MOCK_<RESOURCE>S: <Resource>[] = [
  {
    id: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    title: "Dữ liệu mẫu kiểm thử Wave 1",
    description: "Giúp Frontend kiểm chứng trọn vẹn 4 trạng thái UI khi Backend chưa xong",
    created_at: "2026-10-02T12:00:00Z",
    updated_at: "2026-10-02T12:00:00Z"
  }
];
```

---

## 5. UI & State Architecture — Thiết kế Giao diện (`frontend-dev` — Đích: `src/frontend/`)

- **Cấu trúc Routes (`src/frontend/src/app/...`)**:
  - `page.tsx`: Mặc định là **async Server Component** (data fetching trên server, truyền dữ liệu ban đầu xuống client).
  - `loading.tsx`: Skeleton loader tự động kích hoạt Next.js Suspense Streaming.
  - `error.tsx`: React Error Boundary (`"use client"`) bắt lỗi runtime cấp route kèm nút `reset()`.
  - Component tương tác: Đặt `"use client"` cho component tương tác (form, filter bar, modal), sử dụng React 19 **`useActionState`** và **`useOptimistic`**.
- **TypeScript Interfaces (`src/frontend/src/types/<module>.ts`)**: Khớp 100% với mục 2 và 4. Tuyệt đối không dùng `any`.
- **Quy chuẩn 4 Trạng thái Giao diện (UI States)**:
  1. **Loading**: Hiển thị Skeleton loader tương ứng với layout danh sách/chi tiết.
  2. **Error**: Banner/Alert thông báo lỗi rõ ràng kèm nút "Thử lại" (Retry action).
  3. **Empty**: Giao diện khi không có bản ghi kèm nút hành động (CTA) tạo mới.
  4. **Success**: Render bảng/thẻ responsive, hỗ trợ điều hướng phím và A11y.
- **Tiện ích Styling**: Luôn dùng hàm `cn(...)` từ `@/lib/utils` (`clsx` + `tailwind-merge`) khi xử lý conditional styling.

---

## 6. Ma Trận Truy Xuất Yêu Cầu & Kịch Bản Kiểm Thử (Acceptance Criteria & Test Matrix)

| Tiêu Chí Nghiệm Thu (AC-ID) | Mã PRD (BAC/FR) | Mô Tả Nghiệp Vụ | Mã Test Case (TC-ID) | Tầng Kiểm Thử | Kết Quả Kỳ Vọng |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AC-01** | `BAC-01` / `FR-01` | Tạo tài nguyên với dữ liệu hợp lệ | `TC-01` | Backend API | HTTP 201, trả về đúng schema JSON |
| **AC-02** | `BAC-02` / `FR-02` | Bắt lỗi thiếu trường bắt buộc | `TC-02` | Backend API | HTTP 422, trả về trường vi phạm |
| **AC-03** | `BR-01` | Ràng buộc Unique Constraint | `TC-03` | Database & API | HTTP 409 hoặc database integrity error |
| **AC-04** | `FR-01` (UI) | Hiển thị đầy đủ 4 trạng thái UI | `TC-04` | Frontend Web | Loading skeleton, error retry, empty CTA, data display |
| **AC-05** | NFR / Type | Xác thực kiểu dữ liệu nghiêm ngặt | `TC-05` | Frontend Typecheck | Không có lỗi biên dịch TypeScript, 0 `any` |

---

## 7. Phân rã Công việc theo 2-Wave (Atomic Execution Tasks)

### Wave 1: Dành cho `db-dev` (Phạm vi: `src/db/`)
- [ ] **Task DB-1**: Khởi tạo SQLAlchemy 2.0 model tại `src/db/models/<module>.py` (kế thừa `UUIDPrimaryKeyMixin`).
- [ ] **Task DB-2**: Viết repository async tại `src/db/repositories/<module>.py` (tối ưu `selectinload`).
- [ ] **Task DB-3**: Tạo migration script an toàn tại `src/db/migrations/versions/`.
- [ ] **Task DB-4**: Viết kịch bản seed dữ liệu mẫu idempotent tại `src/db/seeds/<module>_seed.py`.
- [ ] **Task DB-5**: Chạy smoke check: `.venv/bin/ruff check src/db/` và `python3 -m py_compile src/db/...`.

### Wave 1: Dành cho `frontend-dev` (Phạm vi: `src/frontend/`)
- [ ] **Task FE-1**: Khai báo TypeScript types tại `src/frontend/src/types/<module>.ts` khớp chuẩn Hợp đồng.
- [ ] **Task FE-2**: Tạo mock fixtures tại `src/frontend/src/lib/api/mocks/<module>.ts`.
- [ ] **Task FE-3**: Xây dựng Typed API client wrapper tại `src/frontend/src/lib/api/<module>.ts`.
- [ ] **Task FE-4**: Xây dựng UI components & pages xử lý trọn vẹn 4 trạng thái giao diện.
- [ ] **Task FE-5**: Chạy smoke check: `npm --prefix src/frontend run typecheck`.

### Wave 2: Dành cho `backend-dev` (Phạm vi: `src/backend/`, kết nối `src/db/`)
- [ ] **Task BE-1**: Tạo Pydantic v2 schemas tại `src/backend/app/schemas/<module>.py` (`from_attributes=True`).
- [ ] **Task BE-2**: Xây dựng business service tại `src/backend/app/services/<module>.py` kết nối `src/db/`.
- [ ] **Task BE-3**: Tạo API endpoint tại `src/backend/app/api/v1/endpoints/<module>.py` và đăng ký vào router.
- [ ] **Task BE-4**: Chạy smoke check: `.venv/bin/ruff check src/backend/` và `python3 -m py_compile src/backend/...`.

---

## 8. Khai Báo Thư Viện Mới (Dependencies Declaration)
> Nếu không cần thêm thư viện mới, ghi rõ: `Không có thư viện mới phát sinh`.

- **Python (`pyproject.toml`)**:
  - `package-name`: Mục đích sử dụng
- **Frontend (`package.json`)**:
  - `package-name`: Mục đích sử dụng
