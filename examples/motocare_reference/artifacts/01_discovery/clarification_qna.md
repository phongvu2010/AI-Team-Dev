# BIÊN BẢN LÀM RÕ YÊU CẦU KHÁCH HÀNG (CLARIFICATION Q&A)
**Dự án:** MotoCare_Upgrade
**Ngày lập:** 2026-10-10
**Đơn vị thực hiện:** Sub-Team 1 (Client Liaison & BA Agent)

---

## 1. TẦM NHÌN SẢN PHẨM & MỤC TIÊU CỐT LÕI
Hệ thống số hóa toàn diện quy trình cung ứng và đặt hàng Phụ tùng & Dịch vụ Sửa chữa Xe.

## 2. PHÂN ĐỊNH PHẠM VI (SCOPE BOUNDARIES)
### In-Scope (MVP v1.0.0):
- Xác thực người dùng (Đăng ký, Đăng nhập qua JWT, phân quyền Khách hàng & Nhân viên).
- Tra cứu danh mục và bảng giá Phụ tùng & Dịch vụ Sửa chữa Xe.
- Đặt lịch / Đặt hàng dịch vụ trực tuyến và chọn khung giờ xử lý.
- Hệ thống hóa đơn và thanh toán qua mã QR động (VietQR/MoMo).
- Module quản trị dành cho nhân viên xử lý tiếp nhận và tồn kho.

### Out-of-Scope (Dành cho v2.0):
- Tích hợp cổng thanh toán đa quốc gia qua Stripe (dành cho v2.0).
- Hệ thống dự báo nhu cầu bằng AI nâng cao (dành cho v2.0).

## 3. MA TRẬN CÂU HỎI LÀM RÕ (CLARIFICATION Q&A MATRIX)

| Q-ID | Điểm Chưa Rõ Trong Yêu Cầu | Tác Động Kỹ Thuật / Kinh Doanh | Đề Xuất Của AI & Giải Pháp |
|---|---|---|---|
| **Q-01** | Khách hàng có bắt buộc phải đăng nhập trước khi xem danh mục Phụ tùng & Dịch vụ Sửa chữa Xe không? | Ảnh hưởng trực tiếp đến tỷ lệ chuyển đổi đơn hàng và trải nghiệm duyệt ban đầu. | Cho phép xem danh mục và giá công khai; chỉ bắt buộc đăng nhập khi bấm xác nhận đặt hàng. |
| **Q-02** | Phương thức thanh toán trực tuyến ưu tiên trong pha MVP là gì? | Quyết định việc tích hợp cổng thanh toán và xử lý callback trạng thái. | Tích hợp thanh toán chuyển khoản qua mã QR động (VietQR) và thanh toán COD/tiền mặt. |
| **Q-03** | Quy tắc khi số lượng yêu cầu trong một khung giờ vượt giới hạn (Giới hạn tối đa 3 xe mỗi khung giờ (BR-01))? | Nguy cơ quá tải hệ thống và trễ hẹn bàn giao cho khách. | Khóa tự động slot khi đạt ngưỡng tối đa; hiển thị cảnh báo gợi ý khung giờ kế tiếp. |
