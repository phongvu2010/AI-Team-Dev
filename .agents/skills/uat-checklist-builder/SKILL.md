---
name: uat-checklist-builder
description: "Chuyển đổi User Stories và Acceptance Criteria (Gherkin format) thành bảng kiểm thử nghiệm thu người dùng cuối (UAT Checklist) dễ hiểu, không quá kỹ thuật, phục vụ nghiệm thu dự án và bàn giao cho khách hàng / PO."
---

# Kỹ Năng: UAT Checklist Builder (Client Acceptance & Handover)

## 🎯 1. Mục Đích
Kỹ năng này hỗ trợ Tech Lead và BA Agent chuyển hóa các yêu cầu kỹ thuật phức tạp thành một **Bản Kiểm Thử Nghiệm Thu Thân Thiện (UAT Acceptance Checklist)** để:
- Khách hàng hoặc Product Owner phi kỹ thuật có thể tự tay kiểm tra (Manual Visual Testing).
- Đối soát tính năng thực tế với hợp đồng cam kết bàn giao.
- Ký biên bản nghiệm thu bàn giao (Sign-off Acceptance Protocol).

---

## 📋 2. Cấu Trúc Bảng Nghiệm Thu Tiêu Chuẩn

```markdown
# BẢNG KIỂM NGHIỆM THU NGƯỜI DÙNG CUỐI (UAT CHECKLIST)

- **Dự án**: [Tên dự án]
- **Tính năng**: [Tên tính năng / Module]
- **Phiên bản**: v[Version]
- **Người thực hiện kiểm thử**: [Họ và tên Tester / Khách hàng]
- **Ngày kiểm thử**: YYYY-MM-DD

---

### Phần 1: Kiểm Thử Hành Trình Người Dùng (User Journeys)

| Mã UAT | Màn Hình / Chức Năng | Các Bước Thao Tác (Step-by-Step) | Kết Quả Thực Tế Mong Đợi | Trạng Thái | Ghi Chú / Phản Hồi |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **UAT-01** | Đăng ký & Kích hoạt | 1. Mở trang Đăng ký.<br>2. Nhập họ tên, SĐT hợp lệ, mật khẩu.<br>3. Bấm 'Đăng ký ngay'. | • Hệ thống thông báo thành công.<br>• Tự động chuyển hướng vào màn hình Dashboard.<br>• Tên người dùng hiển thị ở góc phải. | [ ] Đạt<br>[ ] Chưa đạt | Giao diện hiển thị nhanh, rõ ràng |
| **UAT-02** | Xem Danh mục & Lọc | 1. Vào trang Danh mục.<br>2. Chọn bộ lọc theo danh mục 'Dịch vụ'.<br>3. Nhập từ khóa tìm kiếm. | • Danh sách chỉ hiển thị đúng các mục khớp điều kiện.<br>• Phân trang hoạt động mượt mà. | [ ] Đạt<br>[ ] Chưa đạt | |
| **UAT-03** | Xử lý Nhập Sai Dữ Liệu | 1. Nhập sai định dạng email hoặc để trống ô bắt buộc.<br>2. Bấm nút Submit. | • Nút bấm bị vô hiệu hóa hoặc xuất hiện dòng cảnh báo màu đỏ dễ hiểu dưới ô nhập.<br>• Không bị treo trang (white screen). | [ ] Đạt<br>[ ] Chưa đạt | |
| **UAT-04** | Trạng Thái Rỗng (Empty) | 1. Truy cập giỏ hàng hoặc lịch sử khi chưa có dữ liệu. | • Hiển thị hình minh họa thân thiện kèm thông điệp 'Chưa có đơn hàng nào'.<br>• Có nút bấm 'Khám phá ngay' dẫn về trang chủ. | [ ] Đạt<br>[ ] Chưa đạt | |

---

### Phần 2: Đánh Giá Trải Nghiệm & Giao Diện (UI/UX Feedback)
- [ ] Giao diện hiển thị chuẩn xác trên cả màn hình Desktop và Mobile (Responsive).
- [ ] Font chữ tiếng Việt sắc nét, không bị lỗi hiển thị (Vn-font integrity).
- [ ] Tốc độ tải trang phản hồi dưới 1 giây đối với các tác vụ thông thường.

---

### Phần 3: Chữ Ký Biên Bản Bàn Giao
- **Đại diện Đội ngũ Kỹ thuật (Antigravity Tech Lead)**: ___________________________
- **Đại diện Khách hàng / Nghiệm thu (Client / PO)**: ___________________________
```

---

## 🛡️ 3. Quy Tắc Biên Soạn
1. **Ngôn ngữ bình dân, phi kỹ thuật**: Tránh dùng các từ như "HTTP 200", "payload JSON", "ORM query", "state hook". Thay vào đó dùng "Màn hình hiển thị thông báo thành công", "Danh sách hiển thị đúng thông tin đã nhập".
2. **Hướng dẫn bước 1-2-3 rõ ràng**: Người dùng không cần kiến thức lập trình vẫn có thể làm theo từng bước để kiểm chứng.
3. **Luôn có cột phản hồi (Feedback/Notes)**: Để khách hàng ghi chú lại các tinh chỉnh về mặt thẩm mỹ hoặc câu chữ cần điều chỉnh nhỏ.
