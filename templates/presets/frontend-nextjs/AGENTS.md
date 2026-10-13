# Frontend Layer Rules (`src/frontend/AGENTS.md`)

Quy tắc bắt buộc khi bất kỳ Agent nào (`frontend-dev`, `qa-tester`, `code-reviewer`) thao tác trong thư mục `src/frontend/`:

---

## 1. Rào Chắn An Toàn Dòng Lệnh & Phân Quyền (CLI Guardrails)
- **Quyền sở hữu File**: Tác tử `frontend-dev` chỉ được tạo và chỉnh sửa file trong `src/frontend/`. Tuyệt đối không can thiệp vào `src/db/` hay `src/backend/`.
- **Lệnh được phép**:
  - `npm --prefix src/frontend run typecheck`
  - `npm --prefix src/frontend run lint`
  - `npm --prefix src/frontend run build`
- **Lệnh cấm tuyệt đối**:
  - Cấm `rm -rf`, `git reset`, `git checkout`.
  - Cấm tự ý sửa `src/frontend/package.json` hay `package-lock.json`. Cấm chạy lệnh `npm install` trần trong sandbox. Khi cần thêm package mới, BẮT BUỘC chỉ cắm cờ `[DEPENDENCY REQUIRED]` để Tech Lead Orchestrator trực tiếp cập nhật.
  - Cấm sửa code ngoài `src/frontend/`.

---

## 2. Tuân Thủ Hợp Đồng API & Dữ Liệu Xuyên Tầng (Contract Alignment)
- Mọi dữ liệu trao đổi với Backend phải được định nghĩa interface rõ ràng tại `src/frontend/src/types/` và khớp 100% với mục **Cross-Layer Data Contract Matrix** và **API Contract** trong `docs/specs/<feature-slug>/plan.md`.
- **Casing**: Interface properties sử dụng thống nhất chuẩn **`snake_case`** theo đúng hợp đồng REST API JSON. Không tự ý đổi tên trường sang `camelCase` khi nhận từ API để tránh lỗi `undefined` tại runtime.
- **Strict TypeScript — Tuyệt đối không dùng `any`**: Mọi props, state, tham số và giá trị trả về đều phải có kiểu tường minh.

---

## 3. Tiêu Chuẩn Kiến Trúc React 19 & Next.js 15 (Server-First & Streaming)

### 3.1. Phân định Data Fetching (Server Component vs Client Component)
- **Mặc định là Server Component**: Mọi `page.tsx` là async Server Component; fetch dữ liệu trực tiếp trên server qua `apiRequest<T>` để tối ưu SEO, streaming và LCP.
- **Client Component tối giản**: Chỉ thêm `"use client"` khi component cần React hooks (`useState`, `useActionState`), event listeners hoặc browser APIs.

### 3.2. Chuẩn mực React 19
- **Form Actions & Mutations**: Ưu tiên sử dụng `useActionState` và `useFormStatus` cho form submission.
- **Optimistic UI**: Dùng `useOptimistic` để cập nhật trạng thái UI ngay lập tức trước khi server phản hồi.
- **Ref as a Prop**: Truyền `ref` trực tiếp như prop (`ref?: React.Ref<T>`). **Tuyệt đối không dùng `forwardRef()`**.
- **Transitions**: Dùng `useTransition` / `startTransition` để wrap các state transitions không khẩn cấp.

### 3.3. Streaming Suspense & 4 Trạng Thái Giao Diện
- **Cấp độ Route**:
  - Bắt buộc tạo `loading.tsx` chứa Skeleton loader để Next.js tự động streaming Suspense.
  - Bắt buộc tạo `error.tsx` (`"use client"`) làm Error Boundary bắt lỗi runtime kèm nút gọi `reset()`.
- **Cấp độ Component**: Bắt buộc xử lý trọn vẹn 4 trạng thái:
  1. **Loading state**: Skeleton loader hoặc spinner tương ứng layout.
  2. **Error state**: Alert thông báo lỗi rõ ràng kèm nút Thử lại (Retry).
  3. **Empty state**: Giao diện khi dữ liệu rỗng kèm nút hành động (CTA) tạo mới.
  4. **Success state**: Render dữ liệu chuẩn xác, responsive trên di động và máy tính.
- **Tiện ích Nối Class Tailwind**: Luôn dùng hàm `cn(...)` từ `@/lib/utils` (kết hợp `clsx` + `tailwind-merge`) khi xử lý conditional classes, tránh nối chuỗi thô gây xung đột CSS specificity.
- **Accessibility (A11y)**: Sử dụng HTML ngữ nghĩa (`<main>`, `<nav>`, `<form>`, `<button>`), mọi ô nhập phải có `<label htmlFor="...">`, nút icon phải có `aria-label`.
- **Client Cache Invalidation (Next.js 15)**: Khi hệ thống chuyển cờ `NEXT_PUBLIC_USE_MOCKS=false` để sang Wave 2 Live API, typed API client (`src/frontend/src/lib/api/client.ts`) tự động áp dụng `cache: 'no-store'` và gọi `clearClientApiCache()` để xóa sạch toàn bộ stale mock cache còn lưu trong trình duyệt.

---

## 4. Tham Gia Vòng Lặp Sửa Lỗi (Feedback Loop Protocol)
Khi nhận tin nhắn điều phối `[SELF-HEALING ACTION REQUIRED]` từ QA hoặc `[REVIEW-FIX ACTION REQUIRED]` từ Reviewer:
1. Phân tích nguyên nhân và **chỉ chỉnh sửa trong phạm vi `src/frontend/`**.
2. Kiểm tra smoke check: `npm --prefix src/frontend run typecheck`.
3. Gửi thông điệp phản hồi `[FIX-COMPLETED]` cho Tech Lead Orchestrator:
   ```text
   [FIX-COMPLETED]
   - Feature: <feature-slug>
   - Iteration: <iteration_number>
   - Target Agent: frontend-dev
   - Modified Files: src/frontend/...
   - Contract Modified: TRUE | FALSE
   - Contract Changes: <chi tiết thay đổi TypeScript interface / client nếu TRUE, hoặc NONE>
   - Resolved Bug/Finding IDs: <BUG-01 hoặc REV-01>
   - Summary of Fix: <mô tả ngắn giải pháp đã thực hiện>
   ```

- **Tiếp nhận Cảnh báo Lệch Schema Sớm (`[CONTRACT-UPDATE NOTICE]`)**: Khi nhận tin nhắn này từ Tech Lead tại Wave Handshake Gate, `frontend-dev` lập tức cập nhật lại TypeScript interfaces tại `src/frontend/src/types/` và mock fixtures tại `src/frontend/src/lib/api/mocks/` theo phiên bản `plan.md` mới nhất, chạy typecheck và phản hồi `[CONTRACT-ALIGNED]`.
