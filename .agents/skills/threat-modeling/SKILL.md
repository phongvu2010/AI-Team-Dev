---
name: threat-modeling
description: "Thực hiện phân tích mô hình mối đe dọa bảo mật theo chuẩn STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege), phòng chống OWASP API Top 10 và xây dựng ma trận phân quyền RBAC & Object-Level Ownership."
---

# Threat Modeling & Security Guardrails Skill

## Mục đích
Hỗ trợ **System Architect / Planner (`planner`)** và **Principal Code Reviewer (`code-reviewer`)** rà soát rủi ro an toàn thông tin ngay từ giai đoạn thiết kế kiến trúc trước khi viết code (Shift-Left Security) và thẩm định bảo mật mã nguồn trong chu trình phát triển của AI Team Dev.

---

## 1. Khung Phân Tích Mối Đe Dọa STRIDE

| Ký Hiệu | Mối Đe Dọa (Threat) | Định Nghĩa & Rủi Ro | Biện Pháp Phòng Thủ Chuẩn (Mitigation in FastAPI / Next.js) |
| :---: | :--- | :--- | :--- |
| **S** | **Spoofing** (Giả mạo) | Kẻ tấn công giả danh người dùng hoặc service khác. | • JWT Token ký bằng thuật toán bảo mật (HS256/RS256) có hạn sử dụng (`exp`).<br>• Hash mật khẩu bằng `argon2id` hoặc `bcrypt`.<br>• Đặt cookie `HttpOnly; Secure; SameSite=Lax`. |
| **T** | **Tampering** (Can thiệp dữ liệu) | Sửa đổi dữ liệu trái phép trên đường truyền hoặc trong cơ sở dữ liệu. | • Bắt buộc HTTPS / TLS 1.3.<br>• Sử dụng Parameterized Queries qua SQLAlchemy ORM 2.0 (chống SQLi tuyệt đối).<br>• Xác thực tính toàn vẹn payload qua Pydantic v2 validation. |
| **R** | **Repudiation** (Chối bỏ hành vi) | Người dùng hoặc hệ thống phủ nhận hành động đã thực hiện. | • Ghi nhận Audit Log bất biến: `user_id`, `action`, `ip_address`, `timestamp` (UTC).<br>• Không cho phép sửa đổi hoặc xóa nhật ký giao dịch tài chính/nhạy cảm. |
| **I** | **Information Disclosure** (Rò rỉ thông tin) | Lộ dữ liệu nhạy cảm qua API response, error stack traces, hoặc log. | • Response Pydantic Schema loại trừ `password_hash`, secret keys.<br>• Tắt debug mode trên môi trường Production (`DEBUG=False`).<br>• Làm sạch (masking) thông tin PII (Email, Phone, CCCD) trong log hệ thống. |
| **D** | **Denial of Service** (Từ chối dịch vụ) | Làm kiệt quệ tài nguyên máy chủ hoặc cơ sở dữ liệu. | • Phân trang bắt buộc (`limit` tối đa 100 bản ghi).<br>• Giới hạn độ dài chuỗi (`max_length`) trong Pydantic schemas.<br>• Rate limiting trên các endpoint nhạy cảm (`/api/v1/auth/login`, `/register`). |
| **E** | **Elevation of Privilege** (Leo thang đặc quyền) | Người dùng thông thường truy cập hoặc can thiệp dữ liệu cấp Admin. | • Dependency Injection kiểm tra Roles & Scopes tại route level.<br>• Kiểm tra quyền sở hữu tài nguyên (Broken Object Level Authorization - BOLA): Chỉ user sở hữu bản ghi mới được phép sửa/xóa. |

---

## 2. Quy Chuẩn Phòng Chống OWASP API Security Top 10

1. **Zero Hardcoded Credentials:**
   - Tuyệt đối nghiêm cấm commit API keys, mật khẩu DB, JWT secret keys vào source code.
   - Mọi bí mật cấu hình phải nạp qua biến môi trường (`.env` và `pydantic-settings`).
2. **Broken Object Level Authorization (BOLA / IDOR):**
   - Khi gọi `GET /api/v1/orders/{order_id}`, backend bắt buộc kiểm tra: `WHERE order.id = :order_id AND (order.user_id = :current_user_id OR current_user.role == 'admin')`.
3. **Broken Authentication:**
   - Khóa tài khoản tạm thời sau số lần đăng nhập sai liên tiếp.
   - Không trả về gợi ý lỗi cụ thể (ví dụ: dùng chung thông báo *"Tên đăng nhập hoặc mật khẩu không chính xác"* thay vì *"Email không tồn tại"*).
4. **Unrestricted Resource Consumption:**
   - Luôn đặt timeout cho HTTP client calls và DB queries.
   - Bắt buộc kiểm soát kích thước payload upload.

---

## 3. Mẫu Ma Trận Phân Quyền & Quyền Sở Hữu (RBAC & Ownership Matrix)

Khi lập `plan.md`, `planner` sử dụng bảng ma trận sau:

```markdown
| Tài Nguyên (Resource) | Hành Động (Action) | Role: Customer | Role: Staff | Role: Admin | Ràng Buộc Quyền Sở Hữu (Ownership Rule) |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `User Profile` | Read / Update | ALLOW | ALLOW | ALLOW | Chỉ xem và sửa profile của chính mình (`user_id == current_user.id`) |
| `Resource Item` | Create | ALLOW | ALLOW | ALLOW | Gán tự động `created_by = current_user.id` |
| `Resource Item` | Read | ALLOW | ALLOW | ALLOW | Public hoặc thuộc quyền sở hữu |
| `Resource Item` | Update / Delete | ALLOW | ALLOW | ALLOW | Bắt buộc `owner_id == current_user.id` (Admin được phép override) |
| `System Settings` | Any | DENY | DENY | ALLOW | Chỉ Admin toàn quyền |
```
