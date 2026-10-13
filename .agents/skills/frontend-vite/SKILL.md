---
name: frontend-vite
description: >-
  React + Vite + TypeScript (Strict) + Tailwind CSS patterns for the Frontend Dev Team (frontend-dev). Activate when building SPA Web clients, dashboards, fast HMR client components, 4 UI states, or responsive layouts in src/frontend/ using the Vite preset.
---

# Frontend Team Runbook: React + Vite + TypeScript + Tailwind CSS

Runbook này hướng dẫn `frontend-dev` xây dựng giao diện ứng dụng web Single Page Application (SPA) hiệu năng cao theo chuẩn **React + Vite + Tailwind CSS**, tuân thủ **Cross-Layer Data Contract Matrix**, rào chắn an toàn dòng lệnh (**CLI Guardrails**), xử lý đủ 4 trạng thái UI và tham gia vòng lặp tự sửa lỗi (**Feedback Loop**).

---

## 1. Rào Chắn An Toàn Dòng Lệnh (CLI Guardrails)
- **Quyền sở hữu**: Chỉ tạo/sửa file trong `src/frontend/`.
- **Lệnh được phép**:
  - `npm --prefix src/frontend run typecheck`
  - `npm --prefix src/frontend run lint`
  - `npm --prefix src/frontend run build`
  - `npm --prefix src/frontend run dev`
- **Quy chuẩn Sandbox**:
  - Cấm chạy `npm install` trần trong sandbox; khi cần thêm package (như `@tanstack/react-query`, `lucide-react`), cắm cờ `[DEPENDENCY REQUIRED]`.

---

## 2. Cấu Trúc Thư Mục Chuẩn (`src/frontend/` — Vite Preset)

```text
src/frontend/
├── index.html                # Entrypoint HTML
├── vite.config.ts            # Cấu hình Vite & alias @/ -> src/
├── tailwind.config.ts        # Cấu hình Tailwind CSS
├── postcss.config.js
├── package.json
├── tsconfig.json
└── src/
    ├── main.tsx              # React DOM render root
    ├── App.tsx               # Root Component & Layout
    ├── index.css             # Tailwind base/components/utilities
    ├── components/           # UI Components tái sử dụng
    ├── lib/
    │   ├── utils.ts          # Helper cn(...) (clsx + tailwind-merge)
    │   └── api/
    │       ├── client.ts     # apiRequest typed fetch client
    │       └── mocks/        # Mock fixtures phục vụ Wave 1
    └── types/                # TypeScript Interfaces (khớp 100% snake_case)
```

---

## 3. Quy Chuẩn Đồng Bộ Hợp Đồng (Contract Synchronization)
1. **Thống nhất Casing `snake_case`**:
   - Tất cả TypeScript interfaces tại `src/frontend/src/types/` phải dùng đúng tên trường `snake_case` khớp 100% với `plan.md`.
2. **Biến môi trường Vite**:
   - Định dạng: `VITE_API_URL`, `VITE_USE_MOCKS`. Truy cập qua `import.meta.env.VITE_API_URL`.
3. **Xử lý 4 Trạng Thái UI**:
   - Mọi màn hình/component data fetching bắt buộc cài đặt đủ 4 trạng thái: Loading (skeleton/spinner), Error (alert + retry), Empty (card + CTA), Success (dữ liệu responsive).
