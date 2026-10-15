# MotoCare_Upgrade — Mobile App (React Native TypeScript)

Ứng dụng di động được xây dựng bằng **React Native**, **TypeScript**, kiến trúc đa màn hình theo chuẩn Tech Lead Profile.

---

## 🚀 Khởi Chạy Nhanh (Quick Start)

### 1. Cài đặt dependencies & khởi động Expo:
```bash
bash setup_dev.sh
# Hoặc:
npm install
npm start
```

### 2. Chạy trên Thiết bị & Giả lập:
- **Android Emulator / Device:** `npm run android`
- **iOS Simulator (macOS):** `npm run ios`

### 3. Kiểm thử (Unit & Logic Tests):
```bash
# Chạy bộ test tương thích Node sandbox:
node run_tests.cjs

# Chạy qua Jest (khi đã cài node_modules):
npm test
```

## 📂 Cấu Trúc Thư Mục
```text
frontend/
├── App.tsx                      # Entrypoint tích hợp AppNavigator
├── types.ts                     # TypeScript Interfaces
├── setup_dev.sh                 # Scaffolding startup script
├── run_tests.cjs                # Standalone Jest assertion runner
├── src/
│   ├── api/client.ts            # Axios REST API Client
│   ├── store/appStore.ts        # Quản lý State tập trung
│   ├── navigation/AppNavigator  # Điều hướng màn hình
│   └── screens/                 # Auth, Catalog, Booking, Tracking Screens
└── __tests__/App.test.tsx       # Jest test suite (3 Unit Tests)
```
