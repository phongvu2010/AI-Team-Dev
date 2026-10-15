# ĐẶT TẢ YÊU CẦU MẪU TỪ KHÁCH HÀNG (SAMPLE CLIENT BRIEF)
> **Mục đích**: File đề bài thực tế giúp bạn thử nghiệm ngay lập tức toàn bộ chu trình 6 giai đoạn của AI Team Dev (từ BA phỏng vấn `ask_question`, Planner thiết kế `plan.md`, Dev Squads lập trình `src/`, QA kiểm thử, đến Code Reviewer).

---

## 1. Thông Tin Chung
- **Tên dự án**: **MotoCare SmartApp** (Nền tảng đặt lịch bảo dưỡng & quản lý sửa chữa xe máy)
- **Khách hàng**: Chuỗi Trung Tâm Dịch Vụ Sửa Chữa Xe Máy Toàn Quốc (MotoCare)
- **Hệ sinh thái mục tiêu**:
  - Web Portal dành cho Nhân viên lễ tân & Quản lý cửa hàng (Next.js 15 / React Vite).
  - Mobile App dành cho Khách hàng sử dụng xe máy (React Native Expo).
  - Backend API hiệu năng cao (Python FastAPI + SQLAlchemy 2.0 + PostgreSQL).

---

## 2. Nỗi Đau Hiện Tại Của Khách Hàng (Pain Points)
1. **Khách hàng mang xe đến tiệm phải chờ đợi hàng giờ** vì không biết tiệm đang quá tải hay còn chỗ trống.
2. **Khách hàng thiếu niềm tin về giá phụ tùng**: Lo sợ bị "chặt chém" hoặc thay thế linh kiện không báo trước.
3. **Cửa hàng thường xuyên bị dồn xe vào các giờ cao điểm** (17h - 19h), dẫn đến thợ làm quá tải, giảm chất lượng sửa chữa.

---

## 3. Các Yêu Cầu Chức Năng Cốt Lõi (In-Scope MVP - P0)

### 3.1. Phân Hệ Dành Cho Khách Hàng (Customer Mobile App)
- **Đăng ký / Đăng nhập**: Xác thực bằng số điện thoại và mật khẩu, cấp phát JWT token.
- **Tra cứu Bảng Giá & Dịch Vụ**: Xem danh mục dịch vụ niêm yết (Thay nhớt, bảo dưỡng toàn diện, làm nồi, rửa xe) kèm giá phụ tùng minh bạch.
- **Đặt Lịch Hẹn Trước (Appointment Booking)**:
  - Chọn dòng xe (Hãng xe, Tên xe, Biển số).
  - Chọn dịch vụ mong muốn.
  - Chọn khung giờ tiếp nhận (ví dụ: 08:30 - 09:00).
- **Theo Dõi Tiến Độ Sửa Chữa (Real-time Tracking)**:
  - Xem trạng thái xe theo thời gian thực: `PENDING` $\to$ `IN_PROGRESS` $\to$ `WAITING_FOR_PARTS` $\to$ `COMPLETED`.
- **Thanh Toán**: Xem hóa đơn chi tiết (tiền dịch vụ + tiền phụ tùng) và thanh toán qua mã QR động (VietQR) hoặc tiền mặt.

### 3.2. Phân Hệ Quản Trị Cửa Hàng (Staff & Admin Web Portal)
- **Điều phối Lịch Hẹn (Slot Management)**:
  - **Quy tắc Nghiệp vụ Bắt buộc (BR-01)**: Mỗi khung giờ 30 phút chỉ tiếp nhận tối đa 3 xe để đảm bảo chất lượng phục vụ. Nếu đã đủ 3 lịch hẹn, hệ thống phải tự động khóa slot đó và gợi ý khung giờ khác.
- **Quản lý Tiếp Nhận Xe**: Cập nhật trạng thái sửa chữa, ghi chú các phụ tùng cần thay thế phát sinh.
- **Quản lý Kho Phụ Tùng**: Theo dõi số lượng tồn kho phụ tùng cơ bản (dầu nhớt, bugi, bố thắng).

---

## 4. Các Tính Năng Dành Cho Tương Lai (Out-of-Scope v2.0 - P1/P2)
- Cứu hộ xe máy khẩn cấp tận nơi (SOS Roadside Assistance).
- Tích hợp cổng thanh toán quốc tế Visa/Mastercard.
- Chương trình tích điểm thành viên đổi quà (Loyalty Program).

---

## 5. Hướng Dẫn Thử Nghiệm Trên Antigravity 2.0 Chat
Để bắt đầu thử nghiệm, bạn chỉ cần copy prompt sau vào khung chat Antigravity:

> *"Tôi có một đề bài khách hàng tại file [`examples/sample_client_brief.md`](file:///d:/Hoang%20Vu/Python%20Project/AI-Team-Dev/examples/sample_client_brief.md). Hãy bắt đầu quy trình với BA Agent để phỏng vấn tôi và bóc tách tính năng Đặt lịch hẹn (Appointment Booking) thành PRD hoàn chỉnh nhé."*
