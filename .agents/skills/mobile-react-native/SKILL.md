---
name: mobile-react-native
description: >-
  React Native, Expo SDK, NativeWind v4 (Tailwind CSS), and TypeScript patterns for the Mobile App Dev Team (frontend-dev). Activate when building iOS and Android screens, native components, Expo Router layouts, typed mobile API clients, or 4 UI states in src/mobile/.
---

# Mobile Team Runbook: React Native + Expo + NativeWind (Tailwind CSS)

Runbook này hướng dẫn `frontend-dev` xây dựng ứng dụng di động đa nền tảng (iOS & Android) theo chuẩn **React Native + Expo SDK + NativeWind (Tailwind CSS)**, tuân thủ **Cross-Layer Data Contract Matrix**, rào chắn an toàn dòng lệnh (**CLI Guardrails**), xử lý đủ 4 trạng thái UI và tham gia vòng lặp tự sửa lỗi (**Feedback Loop**).

---

## 1. Rào Chắn An Toàn Dòng Lệnh (CLI Guardrails)
- **Quyền sở hữu**: Chỉ tạo/sửa file trong `src/mobile/`.
- **Lệnh được phép**:
  - `npm --prefix src/mobile run typecheck`
  - `npm --prefix src/mobile run lint`
  - `npm --prefix src/mobile run start` (hoặc `npx --prefix src/mobile expo start`)
- **Quy chuẩn Sandbox**:
  - Cấm chạy `npm install` trần trong sandbox; khi cần thêm package (như `expo-camera`, `@gorhom/bottom-sheet`, `react-native-reanimated`), cắm cờ `[DEPENDENCY REQUIRED]`.

---

## 2. Cấu Trúc Thư Mục Chuẩn (`src/mobile/`)

```text
src/mobile/
├── app.json                  # Cấu hình Expo App (iOS & Android)
├── metro.config.js           # Metro bundler tích hợp withNativeWind
├── tailwind.config.js        # Cấu hình Tailwind với nativewind/preset
├── global.css                # Tailwind base/components/utilities directives
├── package.json
├── tsconfig.json
├── app/                      # Expo Router (cấu trúc file-based tương tự Next.js)
│   ├── _layout.tsx           # Root stack/tab layout, SafeAreaProvider
│   ├── index.tsx             # Trang chủ mobile
│   └── <feature>/            # Screen tính năng
│       └── [id].tsx
└── src/
    ├── components/           # Reusable Mobile Components
    ├── lib/
    │   └── api/
    │       ├── client.ts     # apiRequest typed mobile fetch client
    │       └── mocks/        # Mock fixtures phục vụ Wave 1
    └── types/                # TypeScript Interfaces (khớp 100% snake_case)
```

---

## 3. Tiêu Chuẩn Lập Trình React Native & NativeWind

### 3.1. Styling với NativeWind
- Dùng `className="..."` trực tiếp trên native components:
  ```tsx
  <View className="flex-1 bg-slate-900 p-6 items-center justify-center">
    <Text className="text-xl font-bold text-white tracking-tight">AI Team Dev Mobile</Text>
    <Text className="text-xs text-slate-400 mt-1">NativeWind Tailwind CSS</Text>
  </View>
  ```

### 3.2. Cấu Hình Địa Chỉ API Đa Thiết Bị (`src/mobile/src/lib/api/client.ts`)
- **Android Emulator**: Loopback IP là `http://10.0.2.2:8000` (thay vì `localhost`).
- **iOS Simulator / Web**: Dùng `http://localhost:8000`.
- **Thiết bị thật (Physical Device)**: Sử dụng IP LAN (ví dụ `http://192.168.1.x:8000`) qua `EXPO_PUBLIC_API_URL`.

### 3.3. Xử Lý Đủ 4 Trạng Thái UI Trên Mobile:
1. **Loading State**: `ActivityIndicator` màu chủ đạo kèm dòng text thông báo đang tải.
2. **Error State**: Card màu đỏ/cam thông báo lỗi mạng kèm nút `Pressable` Thử lại (Retry).
3. **Empty State**: Icon minh họa, text rỗng kèm nút `Pressable` kêu gọi hành động.
4. **Success State**: Render danh sách cuộn (`ScrollView` hoặc `FlatList`) với responsive layout phù hợp màn hình điện thoại.
