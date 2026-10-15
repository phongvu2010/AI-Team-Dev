# PRODUCT REQUIREMENTS DOCUMENT (PRD) - v1.0.0
**Dự án:** MotoCare_Upgrade
**Tác giả:** Business Analyst Agent & Tech Lead
**Ngày ban hành:** 2026-10-10
**Trạng thái:** DRAFT HOÀN CHỈNH (Chờ phê duyệt tại Gate 1)

---

## 1. TỔNG QUAN & MỤC TIÊU ĐỊNH LƯỢNG (SMART GOALS)
- **Tầm nhìn sản phẩm:** Hệ thống số hóa toàn diện quy trình cung ứng và đặt hàng Phụ tùng & Dịch vụ Sửa chữa Xe.
- **Mục tiêu SMART:**
  - Giảm 70% thời gian xử lý đơn hàng và phục vụ khách hàng mua Phụ tùng & Dịch vụ Sửa chữa Xe.
  - Minh bạch 100% bảng giá và trạng thái xử lý đơn hàng theo thời gian thực.
  - Tuân thủ triệt để quy tắc vận hành cốt lõi: Giới hạn tối đa 3 xe mỗi khung giờ (BR-01).

---

## 2. MA TRẬN TÍNH NĂNG CHỨC NĂNG (FUNCTIONAL REQUIREMENTS)

| Mã Tính Năng | Tên Tính Năng | Mô Tả Tóm Tắt | Độ Ưu Tiên | Sub-Team Phụ Trách |
|---|---|---|---|---|
| **FR-01** | Xác thực & Phân quyền RBAC | Hỗ trợ đăng ký, đăng nhập JWT, phân quyền Customer, Staff, Admin | P0 (Must Have) | Backend & Mobile |
| **FR-02** | Quản lý Đơn hàng & Lịch hẹn Phụ tùng & Dịch vụ Sửa chữa Xe | Tiếp nhận và kiểm soát dung lượng theo quy tắc: Giới hạn tối đa 3 xe mỗi khung giờ (BR-01) | P0 (Must Have) | Backend & Mobile |
| **FR-03** | Quản lý Danh mục & Bảng giá | Tra cứu, cập nhật tồn kho và giá bán của Phụ tùng & Dịch vụ Sửa chữa Xe | P0 (Must Have) | Backend & Mobile |
| **FR-04** | Hóa đơn & Thanh toán QR | Tự động tính tổng tiền dịch vụ và sinh mã QR động thanh toán chuyển khoản | P0 (Must Have) | Backend |

---

## 3. DANH MỤC QUY TẮC NGHIỆP VỤ (BUSINESS RULES)

| Mã Quy Tắc | Tên Quy Tắc | Nội Dung Ràng Buộc | Tầng Xử Lý |
|---|---|---|---|
| **BR-01** | Ràng buộc giới hạn công suất | Giới hạn tối đa 3 xe mỗi khung giờ (BR-01) | Service |
| **BR-02** | Thời hạn hiệu lực Access Token | JWT Access Token có thời hạn tối đa 15 phút, ký thuật toán HS256 | Core Security |

---

## 4. DANH SÁCH USER STORIES (VỚI TIÊU CHÍ GHERKIN)
### US-01: Đăng ký & Đăng nhập Người Dùng (MUST_HAVE - 3 pts)
- **As a:** Khách hàng
- **I want to:** Đăng ký và đăng nhập nhanh bằng số điện thoại và mật khẩu
- **So that:** Tôi có thể theo dõi lịch sử và trạng thái đơn hàng của mình
- **Acceptance Criteria (Gherkin):**
```gherkin
Scenario: Đăng ký tài khoản mới thành công
  Given số điện thoại '0912345678' chưa từng đăng ký
  When người dùng nhập họ tên và mật khẩu hợp lệ
  Then hệ thống tạo tài khoản mới và trả về HTTP 201 kèm Access Token JWT

Scenario: Đăng ký trùng số điện thoại
  Given số điện thoại '0912345678' đã tồn tại trong DB
  When người dùng cố gắng đăng ký lại
  Then hệ thống từ chối với HTTP 409 Conflict và thông báo lỗi rõ ràng
```

### US-02: Đặt hàng / Đặt lịch Phụ tùng & Dịch vụ Sửa chữa Xe (MUST_HAVE - 5 pts)
- **As a:** Khách hàng
- **I want to:** Chọn dịch vụ Phụ tùng & Dịch vụ Sửa chữa Xe và chọn thời gian thực hiện
- **So that:** Đơn hàng của tôi được chuẩn bị chu đáo và không bị chờ đợi
- **Acceptance Criteria (Gherkin):**
```gherkin
Scenario: Đặt dịch vụ vào khung giờ còn trống
  Given khung giờ được chọn còn slot trống hợp lệ
  When người dùng bấm xác nhận đặt đơn
  Then hệ thống tạo đơn với trạng thái 'CONFIRMED' và trừ 1 slot còn trống

Scenario: Từ chối khi vượt công suất (Giới hạn tối đa 3 xe mỗi khung giờ (BR-01))
  Given khung giờ đã đạt ngưỡng giới hạn tối đa
  When người dùng cố gắng đặt thêm
  Then hệ thống từ chối với HTTP 400 Bad Request và thông báo 'Khung giờ đã đầy chỗ'
```

### US-03: Tra cứu Bảng Giá Phụ tùng & Dịch vụ Sửa chữa Xe (MUST_HAVE - 3 pts)
- **As a:** Khách hàng và Nhân viên
- **I want to:** Xem danh mục mặt hàng niêm yết minh bạch kèm hình ảnh và đơn giá
- **So that:** Tôi nắm rõ chi phí chính xác trước khi ra quyết định mua hàng
- **Acceptance Criteria (Gherkin):**
```gherkin
Scenario: Tra cứu danh mục sản phẩm công khai
  Given hệ thống có danh mục sản phẩm đang hoạt động
  When người dùng gửi yêu cầu GET /api/v1/catalog
  Then hệ thống trả về danh sách sản phẩm HTTP 200 kèm đơn giá niêm yết
```

