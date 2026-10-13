---
name: frontend-nextjs
description: >-
  React 19, Next.js 15 (App Router), TypeScript (Strict), and Tailwind CSS patterns for the Frontend Dev Team (frontend-dev). Activate when building Server & Client Components, typed API clients, React 19 actions, 4 UI states, or responsive layouts in src/frontend/.
---

# Frontend Team Runbook: React 19 + Next.js 15 (App Router) + TypeScript + Tailwind CSS

Runbook này hướng dẫn `frontend-dev` xây dựng giao diện người dùng hiện đại theo chuẩn **React 19 & Next.js 15 (App Router)**, tuân thủ **Cross-Layer Data Contract Matrix**, rào chắn an toàn dòng lệnh (**CLI Guardrails**), tận dụng cơ chế Streaming Suspense và tham gia vòng lặp tự sửa lỗi (**Feedback Loop**).

---

## 1. Rào Chắn An Toàn Dòng Lệnh & Sandbox Guardrails (CLI Guardrails)
- **Quyền sở hữu**: Chỉ tạo/sửa file trong `src/frontend/`.
- **Lệnh được phép**:
  - `npm --prefix src/frontend run typecheck` (Kiểm tra kiểu tĩnh siêu tốc cho Phase 2 & Phase 3)
  - `npm --prefix src/frontend run lint`
  - `npm --prefix src/frontend run build` (Tích hợp `NEXT_TELEMETRY_DISABLED=1` chạy offline chuẩn sandbox)
- **Quy chuẩn Sandbox An Toàn Tuyệt Đối**:
  - Cấm chạy `npm install` trần trong sandbox; khi cần thêm package, cắm cờ `[DEPENDENCY REQUIRED]` để Tech Lead cập nhật.
  - Cấm import external remote fonts (`next/font/google`) vì gây timeout trong môi trường sandbox chặn mạng; luôn dùng system fonts hoặc Tailwind CSS sans utility classes.
  - Cấm sửa file ngoài `src/frontend/`.

---

## 2. Cấu Trúc Thư Mục Chuẩn (`src/frontend/`)

```text
src/frontend/
├── src/
│   ├── app/                  # Next.js 15 App Router
│   │   ├── layout.tsx        # Root layout chung
│   │   ├── page.tsx          # Server Component render trang chủ
│   │   ├── loading.tsx       # Route-level Suspense Streaming Skeleton
│   │   ├── error.tsx         # Route-level Error Boundary ("use client")
│   │   └── <feature>/        # Route segment cho tính năng
│   │       ├── page.tsx      # Async Server Component (Data Fetching)
│   │       ├── loading.tsx   # Feature Skeleton Loader
│   │       └── error.tsx     # Feature Error Boundary
│   ├── components/           # UI Components tái sử dụng & Feature Components
│   │   ├── ui/               # Primitives (Button, Input, Card, Modal, Skeleton)
│   │   └── <feature>/        # Client Components tương tác
│   ├── lib/
│   │   ├── utils.ts          # Helper cn(...) (clsx + tailwind-merge)
│   │   └── api/              # Typed Fetch Client kết nối FastAPI Backend
│   │       ├── client.ts     # apiRequest wrapper (hỗ trợ Server & Client)
│   │       └── mocks/        # Mock fixtures phục vụ Wave 1
│   ├── hooks/                # Custom React Hooks
│   └── types/                # TypeScript Interfaces khớp 100% với Backend Schemas
├── package.json
└── tsconfig.json
```

---

## 3. Quy Chuẩn Đồng Bộ Hợp Đồng (Contract Synchronization)

1. **Thống nhất Casing `snake_case`**:
   - Khai báo interface properties trong `src/frontend/src/types/` theo đúng chuẩn `snake_case` của REST API JSON.
   - Không tự ý đổi tên trường sang `camelCase` khi nhận từ API để tránh lỗi `undefined` tại runtime.
2. **Strict TypeScript — Tuyệt đối không dùng `any`**:
   ```typescript
   export interface Item {
     id: string; // RFC 4122 UUID
     title: string;
     description: string | null;
     tags: string[];
     is_active: boolean;
     created_at: string; // ISO 8601 UTC
     updated_at: string;
   }
   ```
3. **Mẫu Typed API Client Wrapper (`src/frontend/src/lib/api/client.ts`)**:
   ```typescript
   const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

   export function isMockMode(): boolean {
     return process.env.NEXT_PUBLIC_USE_MOCKS === "true";
   }

   export class ApiError extends Error {
     constructor(
       public status: number,
       public detail: string,
     ) {
       super(detail);
       this.name = "ApiError";
     }
   }

   export interface ApiRequestOptions extends RequestInit {
     mockData?: unknown;
     invalidateCache?: boolean;
   }

   export function clearClientApiCache(): void {
     if (typeof window !== "undefined") {
       // Xóa sạch storage cache liên quan API
       sessionStorage.clear();
     }
   }

   export async function apiRequest<T>(
     endpoint: string,
     options?: ApiRequestOptions,
   ): Promise<T> {
     if (isMockMode() && options?.mockData !== undefined) {
       return options.mockData as T;
     }

     const { mockData: _, invalidateCache, ...fetchOptions } = options ?? {};
     // Next.js 15: Mặc định cache 'no-store' khi chạy Live API để triệt tiêu stale mock/cache
     const cacheStrategy: RequestCache =
       fetchOptions.cache ?? (invalidateCache || !isMockMode() ? "no-store" : "default");

     const response = await fetch(`${API_BASE_URL}${endpoint}`, {
       ...fetchOptions,
       cache: cacheStrategy,
       headers: {
         "Content-Type": "application/json",
         ...(invalidateCache || !isMockMode() ? { "Cache-Control": "no-cache" } : {}),
         ...fetchOptions.headers,
       },
     });
   ```

     if (!response.ok) {
       let detail = `HTTP Error ${response.status}`;
       try {
         const errBody = (await response.json()) as { detail?: string };
         if (typeof errBody.detail === "string") {
           detail = errBody.detail;
         }
       } catch {
         // Giữ message mặc định nếu không phải JSON
       }
       throw new ApiError(response.status, detail);
     }

     if (response.status === 204) {
       return undefined as T;
     }

     return (await response.json()) as T;
   }
   ```

---

## 4. Mô Hình Kiến Trúc React 19 & Next.js 15: Server Component-First

### 4.1. Pattern 1: Async Server Component (Mặc định cho Mọi Route / Page)
Thực hiện data fetching trực tiếp trên server, không cần `"use client"`, không cần `useEffect`:

```typescript
// src/frontend/src/app/products/page.tsx
import { apiRequest } from "@/lib/api/client";
import { Product } from "@/types/product";
import { ProductListClient } from "@/components/products/ProductListClient";

async function getProducts(): Promise<Product[]> {
  // Có thể dùng mock trong Wave 1 hoặc gọi API live
  if (process.env.NEXT_PUBLIC_USE_MOCKS === "true") {
    const { mockProducts } = await import("@/lib/api/mocks/products");
    return mockProducts;
  }
  return apiRequest<Product[]>("/api/v1/products");
}

export default async function ProductsPage() {
  const products = await getProducts();

  return (
    <main className="container mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Quản Lý Sản Phẩm
        </h1>
        <p className="text-sm text-slate-600">
          Danh sách sản phẩm được đồng bộ thời gian thực từ cơ sở dữ liệu.
        </p>
      </header>

      {/* Truyền dữ liệu ban đầu xuống Client Component để tương tác */}
      <ProductListClient initialProducts={products} />
    </main>
  );
}
```

### 4.2. Pattern 2: Client Component với React 19 Actions (`useActionState`, `useOptimistic`)
Dành cho component cần tương tác, lọc dữ liệu hoặc mutation:

```typescript
// src/frontend/src/components/products/ProductListClient.tsx
"use client";

import { useOptimistic, useTransition, useState } from "react";
import { Product } from "@/types/product";
import { cn } from "@/lib/utils";
import { apiRequest } from "@/lib/api/client";

interface ProductListClientProps {
  initialProducts: Product[];
}

export function ProductListClient({ initialProducts }: ProductListClientProps) {
  const [products, setProducts] = useState<Product[]>(initialProducts);
  const [isPending, startTransition] = useTransition();

  // React 19: Optimistic UI cập nhật tức thì
  const [optimisticProducts, setOptimisticProducts] = useOptimistic(
    products,
    (current, update: { id: string; is_active: boolean }) =>
      current.map((p) => (p.id === update.id ? { ...p, is_active: update.is_active } : p))
  );

  const handleToggleActive = (id: string, currentStatus: boolean) => {
    const nextStatus = !currentStatus;

    startTransition(async () => {
      // 1. Cập nhật optimistic ngay lập tức
      setOptimisticProducts({ id, is_active: nextStatus });

      try {
        // 2. Gửi request lên server
        const updated = await apiRequest<Product>(`/api/v1/products/${id}`, {
          method: "PATCH",
          body: JSON.stringify({ is_active: nextStatus }),
        });
        setProducts((prev) => prev.map((p) => (p.id === id ? updated : p)));
      } catch (err) {
        // Rollback nếu có lỗi mạng
        console.error("Lỗi cập nhật sản phẩm:", err);
        setProducts([...products]);
      }
    });
  };

  // Trạng thái Empty
  if (optimisticProducts.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 p-12 text-center">
        <h3 className="text-base font-semibold text-slate-900">Chưa có sản phẩm nào</h3>
        <p className="mt-1 text-sm text-slate-500">Bắt đầu bằng việc thêm sản phẩm đầu tiên của bạn.</p>
      </div>
    );
  }

  // Trạng thái Success
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {optimisticProducts.map((product) => (
        <div
          key={product.id}
          className={cn(
            "rounded-xl border p-4 shadow-sm transition-all",
            product.is_active ? "border-slate-200 bg-white" : "border-slate-100 bg-slate-50 opacity-75"
          )}
        >
          <div className="flex items-center justify-between">
            <h4 className="font-medium text-slate-900">{product.title}</h4>
            <button
              type="button"
              disabled={isPending}
              onClick={() => handleToggleActive(product.id, product.is_active)}
              aria-label={`Chuyển trạng thái sản phẩm ${product.title}`}
              className={cn(
                "rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors",
                product.is_active
                  ? "bg-emerald-50 text-emerald-700 hover:bg-emerald-100"
                  : "bg-slate-200 text-slate-600 hover:bg-slate-300"
              )}
            >
              {product.is_active ? "Đang bán" : "Tạm ẩn"}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
```

### 4.3. Pattern 3: React 19 `ref` as a Prop
Trong React 19, `ref` được truyền trực tiếp như prop, không dùng `forwardRef()`:

```typescript
// src/frontend/src/components/ui/Input.tsx
import { InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  ref?: React.Ref<HTMLInputElement>; // React 19 trực tiếp hỗ trợ ref
}

export function Input({ label, error, ref, className, id, ...props }: InputProps) {
  const inputId = id ?? label.toLowerCase().replace(/\s+/g, "-");

  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={inputId} className="text-xs font-medium text-slate-700">
        {label}
      </label>
      <input
        id={inputId}
        ref={ref}
        className={cn(
          "rounded-lg border px-3 py-2 text-sm outline-none transition-colors",
          error
            ? "border-rose-500 focus:border-rose-600"
            : "border-slate-200 focus:border-slate-900",
          className
        )}
        {...props}
      />
      {error && <span className="text-xs text-rose-600">{error}</span>}
    </div>
  );
}
```

---

## 5. Cơ Chế Streaming Suspense & 4 Trạng Thái UI

### 5.1. Cấp độ Route Segment: `loading.tsx` và `error.tsx`
- **`loading.tsx` (Tự động kích hoạt Suspense Streaming)**:
  ```typescript
  // src/frontend/src/app/products/loading.tsx
  export default function ProductsLoading() {
    return (
      <main className="container mx-auto px-4 py-8 animate-pulse">
        <div className="h-8 w-48 rounded bg-slate-200 mb-2" />
        <div className="h-4 w-96 rounded bg-slate-100 mb-8" />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="h-28 rounded-xl bg-slate-100 p-4 border border-slate-200" />
          ))}
        </div>
      </main>
    );
  }
  ```

- **`error.tsx` (Error Boundary cấp Route — Bắt buộc `"use client"`)**:
  ```typescript
  // src/frontend/src/app/products/error.tsx
  "use client";

  export default function ProductsError({
    error,
    reset,
  }: {
    error: Error & { digest?: string };
    reset: () => void;
  }) {
    return (
      <main className="container mx-auto px-4 py-16 text-center">
        <div className="mx-auto max-w-md rounded-2xl border border-rose-200 bg-rose-50/50 p-6">
          <h2 className="text-base font-semibold text-rose-900">Không thể tải dữ liệu sản phẩm</h2>
          <p className="mt-2 text-xs text-rose-600">{error.message || "Đã xảy ra lỗi không xác định."}</p>
          <button
            type="button"
            onClick={() => reset()}
            className="mt-4 rounded-lg bg-rose-600 px-4 py-2 text-xs font-semibold text-white hover:bg-rose-700"
          >
            Thử lại
          </button>
        </div>
      </main>
    );
  }
  ```

### 5.2. Cấp độ Component (Bắt buộc Xử lý Đủ 4 Trạng Thái):
1. **Loading State**: Skeleton loader tương ứng layout danh sách/chi tiết.
2. **Error State**: Alert/Banner thông báo lỗi rõ ràng kèm nút Thử lại (Retry).
3. **Empty State**: Giao diện khi dữ liệu rỗng kèm nút kêu gọi hành động (CTA) tạo mới.
4. **Success State**: Render dữ liệu responsive, thân thiện di động và desktop.

---

## 6. Tiện Ích Chuẩn Nối Class Tailwind: `cn(...)`
Được đặt tại `src/frontend/src/lib/utils.ts`:
```typescript
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
```
**Quy tắc**: Tuyệt đối không dùng template literals để nối chuỗi class (`className={`p-4 ${isActive ? 'bg-black' : ''}`}`) để tránh lỗi xung đột độ ưu tiên (specificity) trong Tailwind.

---

## 7. Tham Gia Vòng Lặp Sửa Lỗi (Feedback Loop Protocol)
Khi nhận tin nhắn `[SELF-HEALING ACTION REQUIRED]` từ QA hoặc `[REVIEW-FIX ACTION REQUIRED]` từ Reviewer:
1. Xác định nguyên nhân (lỗi typecheck, thiếu loading/error state, lỗi mock data, hoặc vi phạm React 19 pattern).
2. Sửa lỗi trong `src/frontend/`, chạy `npm --prefix src/frontend run typecheck`.
3. Phản hồi cho Tech Lead bằng thông điệp `[FIX-COMPLETED]`:
   ```text
   [FIX-COMPLETED]
   - Feature: <feature-slug>
   - Iteration: <iteration_number>
   - Target Agent: frontend-dev
   - Modified Files: <danh sách files đã sửa>
   - Contract Modified: TRUE | FALSE
   - Contract Changes: <chi tiết thay đổi TypeScript interface / client nếu TRUE, hoặc NONE>
   - Resolved Bug/Finding IDs: <BUG-01, ...>
   - Summary of Fix: <tóm tắt ngắn gọn giải pháp>
   ```
