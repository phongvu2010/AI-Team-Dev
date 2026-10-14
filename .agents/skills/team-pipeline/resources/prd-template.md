---
feature_slug: "<feature-slug>"
version: "1.0.0"
artifact_type: "prd"
author: "ba"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
status: "DRAFT" # DRAFT | PENDING_REVIEW | APPROVED_BY_USER
iteration: 1
---

# Product Requirements Document (PRD): `<Feature Name>`

> **Tài liệu Yêu cầu Sản phẩm & Đặc tả Nghiệp vụ (PRD)**: Được biên soạn bởi BA Agent (`ba`) thông qua quá trình phỏng vấn và làm rõ yêu cầu với người dùng. Tài liệu này đóng vai trò làm **Cơ sở Nghiệp vụ (Business SSOT)** để `planner` kiến tạo bản thiết kế kỹ thuật (`plan.md`).

---

## 1. Tổng Quan & Mục Tiêu Kinh Doanh (Executive Summary & Objectives)

### 1.1. Bối cảnh & Vấn đề (Problem Statement)
- **Vấn đề hiện tại**: <Mô tả nỗi đau của người dùng hoặc điểm nghẽn trong hệ thống hiện tại>
- **Giải pháp đề xuất**: <Mô tả giải pháp tính năng ở mức nghiệp vụ>

### 1.2. Mục tiêu Kinh doanh (Business Goals & KPIs)
- **Mục tiêu chính**: <Mục tiêu cụ thể đạt được khi tính năng ra mắt>
- **Chỉ số đo lường (KPIs / Success Metrics)**:
  - *KPI 1*: <Ví dụ: Giảm 50% thời gian tạo bài viết>
  - *KPI 2*: <Ví dụ: 0% lỗi mất dữ liệu khi chuyển trang>

### 1.3. Ma Trận Bóc Tách Quy Mô (Epic Decomposition & Granular Feature Slicing)
> ℹ️ *Điền mục này nếu yêu cầu ban đầu của người dùng là một Epic hoặc hệ thống phức hợp lớn.*

- **Định danh Epic cha**: `<epic-slug>`
- **Định cỡ (T-Shirt Size)**: `Size S` | `Size M` | `Size L` | `Size XL`
- **Lộ trình Bóc tách Lát cắt (Slicing Roadmap)**:
| Lát cắt / Feature Slug | Tên Phân Hệ | Phạm vi Nghiệp vụ Tóm tắt | Phân kỳ Triển khai | Trạng thái Hiện tại |
| :--- | :--- | :--- | :---: | :---: |
| `<current-feature-slug>` | Phân hệ cốt lõi MVP | <Tóm tắt phạm vi của PRD hiện tại> | **Phase 1 (P0)** | 🟡 **ACTIVE (Hiện tại)** |
| `<child-feature-slug-2>` | Phân hệ mở rộng / Nâng cao | <Tóm tắt phạm vi tiếp theo> | Phase 2 (P1) | ⚪ Queued |
| `<child-feature-slug-3>` | Phân hệ tích hợp / Báo cáo | <Tóm tắt phạm vi tương lai> | Phase 3 (P2) | ⚪ Backlog |

---

## 2. Chân Dung Người Dùng & Hành Trình (User Personas & User Journeys)

### 2.1. Đối tượng Người dùng (User Personas)
| Persona | Vai trò / Quyền hạn | Mục tiêu chính | Nỗi đau thường gặp |
| :--- | :--- | :--- | :--- |
| **P-01: End User** | Người dùng cuối thông thường | Sử dụng tính năng nhanh chóng, trực quan | Giao diện rườm rà, phản hồi chậm |
| **P-02: Admin / Manager** | Quản trị viên hệ thống | Giám sát, quản lý dữ liệu, phân quyền | Thiếu báo cáo kiểm toán, dữ liệu bị sai lệch |

### 2.2. Hành Trình Người Dùng Điển Hình (Core User Journey)
```text
[Khởi đầu: Người dùng truy cập trang]
       │
       ▼
[Bước 1: Người dùng thực hiện thao tác chính (e.g. Nhập dữ liệu / Bấm nút)]
       │
       ▼
[Bước 2: Hệ thống phản hồi trạng thái (Loading -> Validation -> Xác nhận)]
       │
       ▼
[Kết quả: Dữ liệu được lưu trữ, UI chuyển trạng thái thành công và hiển thị phản hồi]
```

---

## 3. Yêu Cầu Chức Năng & Quy Tắc Nghiệp Vụ (Functional Requirements & Business Rules)

### 3.1. Danh mục Yêu cầu Chức năng (Functional Requirements - FRs)
| Mã FR | Tên chức năng | Persona | Mô tả chi tiết hành vi | Độ ưu tiên |
| :--- | :--- | :--- | :--- | :---: |
| **FR-01** | `<Tên chức năng 1>` | End User | <Mô tả chi tiết những gì hệ thống phải làm> | P0 (Must) |
| **FR-02** | `<Tên chức năng 2>` | End User | <Mô tả chi tiết những gì hệ thống phải làm> | P0 (Must) |
| **FR-03** | `<Tên chức năng 3>` | Admin | <Mô tả chi tiết những gì hệ thống phải làm> | P1 (Should) |

### 3.2. Quy tắc Nghiệp vụ (Business Rules - BRs)
- **BR-01**: <Quy tắc kiểm tra hợp lệ, ví dụ: Tiêu đề không được để trống, độ dài từ 3 đến 255 ký tự>.
- **BR-02**: <Quy tắc quyền hạn, ví dụ: Chỉ người tạo hoặc Admin mới có quyền xóa tài nguyên>.
- **BR-03**: <Quy tắc trạng thái, ví dụ: Đơn hàng ở trạng thái 'Đã hủy' không thể chuyển về 'Đang xử lý'>.

---

## 4. Quản Lý Phạm Vi (Scope Management)

### 4.1. Trong phạm vi phiên bản này (In-Scope - MVP / Phase 1)
- [x] Triển khai toàn bộ các yêu cầu chức năng P0 (`FR-01`, `FR-02`).
- [x] Xử lý đầy đủ 4 trạng thái giao diện (Loading, Error, Empty, Success).
- [x] Xác thực dữ liệu 2 đầu (Client-side validation & Backend schema validation).

### 4.2. Ngoài phạm vi phiên bản này (Out-of-Scope - Future Phases)
- [ ] Tích hợp thông báo qua bên thứ 3 (Email / SMS / Webhook) -> Dời sang Phase 2.
- [ ] Tính năng xuất file Excel / PDF báo cáo thống kê -> Dời sang Phase 2.
- [ ] Hỗ trợ đa ngôn ngữ quốc tế (i18n) -> Dời sang Phase 3.

---

## 5. Yêu Cầu Phi Chức Năng (Non-Functional Requirements - NFRs)

- **Hiệu năng (Performance)**:
  - Thời gian phản hồi API trung bình < 200ms với 95th percentile.
  - Tải trang ban đầu < 1.5s trên mạng 4G tiêu chuẩn.
- **Bảo mật & Phân quyền (Security & Compliance)**:
  - Xác thực người dùng qua JWT/Session, kiểm tra phân quyền chặt chẽ trên từng endpoint.
  - Ngăn chặn SQL Injection, XSS, CSRF; không lộ dữ liệu nhạy cảm qua API response.
- **Khả năng sử dụng & Tiếp cận (Usability & Accessibility - A11y)**:
  - Hỗ trợ thao tác phím (Keyboard navigation) và Screen Reader cơ bản (ARIA labels).
  - Tương thích tốt trên cả Desktop (1920x1080) và Mobile (375x667).

---

## 6. Các Kịch Bản Góc & Xử Lý Ngoại Lệ (Edge Cases & Exception Handling)

| Mã EC | Tình huống góc (Edge Case) | Hành vi mong đợi của Hệ thống |
| :--- | :--- | :--- |
| **EC-01** | Người dùng gửi form nhiều lần liên tiếp (Double Submit / Network Lag) | Nút hành động bị vô hiệu hóa (disabled) ngay khi bấm; hệ thống có cơ chế Idempotency chống tạo trùng. |
| **EC-02** | Dữ liệu đầu vào chứa ký tự đặc biệt hoặc emoji độ dài lớn | Hệ thống xử lý an toàn chuỗi UTF-8, sanitize dữ liệu, không làm vỡ giao diện hoặc lỗi DB. |
| **EC-03** | Mất kết nối mạng giữa chừng khi đang submit | Hiển thị thông báo thân thiện (Alert), lưu tạm bản nháp (Draft) nếu cần, cho phép bấm Retry. |
| **EC-04** | Người dùng cố tình truy cập tài nguyên không thuộc quyền sở hữu | Phản hồi lỗi `403 Forbidden` chuẩn hóa, không để lộ cấu trúc ID nội bộ. |

---

## 7. Tiêu Chí Nghiệm Thu Nghiệp Vụ (Business Acceptance Criteria - BAC)

> Các tiêu chí nghiệm thu này là cơ sở để `planner` chuyển hóa thành Technical Acceptance Criteria (`AC-xx`) và `qa-tester` viết bài test (`TC-xx`).

### BAC-01: `<Tên tiêu chí 1>`
- **Given (Tiền điều kiện)**: Người dùng đã đăng nhập với vai trò `<Role>` và đang ở trang `<Page>`.
- **When (Hành động)**: Người dùng nhập đầy đủ thông tin hợp lệ và nhấn nút `<Button>`.
- **Then (Kết quả mong đợi)**:
  - Hệ thống hiển thị thông báo thành công.
  - Dữ liệu mới xuất hiện ngay trên danh sách mà không cần tải lại toàn bộ trang.

### BAC-02: `<Tên tiêu chí 2>`
- **Given (Tiền điều kiện)**: Người dùng đang ở form nhập liệu.
- **When (Hành động)**: Người dùng bỏ trống trường bắt buộc hoặc nhập sai định dạng và nhấn submit.
- **Then (Kết quả mong đợi)**:
  - Hệ thống không gửi request, hiển thị thông báo lỗi cụ thể ngay dưới trường nhập liệu tương ứng.

---

## 8. Nhật Ký Phỏng Vấn & Làm Rõ Yêu Cầu (Clarification & Interview Log)

| Thời gian | Câu hỏi từ BA (`ask_question`) | Phản hồi từ User | Quyết định Nghiệp vụ thống nhất |
| :--- | :--- | :--- | :--- |
| YYYY-MM-DD | <Câu hỏi làm rõ nghiệp vụ hoặc lựa chọn edge case> | <Câu trả lời của User> | <Quy tắc nghiệp vụ được bổ sung vào PRD> |
