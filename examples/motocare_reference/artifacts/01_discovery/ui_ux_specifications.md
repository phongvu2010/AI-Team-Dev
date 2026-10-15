# ĐẶC TẢ TRẢI NGHIỆM GIAO DIỆN (UI/UX SPECIFICATIONS)
**Dự án:** MotoCare_Upgrade

## 1. SƠ ĐỒ ĐIỀU HƯỚNG MÀN HÌNH (NAVIGATION FLOW)

```mermaid
graph TD
    S1["Màn hình Đăng nhập & Đăng ký (AuthScreen)"]
    S2["Màn hình Khám phá & Danh mục Phụ tùng & Dịch vụ Sửa chữa Xe (CatalogScreen)"]
    S3["Màn hình Đặt lịch / Đặt hàng (BookingScreen)"]
    S4["Màn hình Theo dõi Trạng thái đơn hàng Realtime (TrackingScreen)"]
    S5["Màn hình Quản trị Đơn hàng & Kho dành cho Nhân viên (AdminDashboard)"]
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
```

## 2. DANH SÁCH MÀN HÌNH
- **Màn hình Đăng nhập & Đăng ký (AuthScreen)**
- **Màn hình Khám phá & Danh mục Phụ tùng & Dịch vụ Sửa chữa Xe (CatalogScreen)**
- **Màn hình Đặt lịch / Đặt hàng (BookingScreen)**
- **Màn hình Theo dõi Trạng thái đơn hàng Realtime (TrackingScreen)**
- **Màn hình Quản trị Đơn hàng & Kho dành cho Nhân viên (AdminDashboard)**
