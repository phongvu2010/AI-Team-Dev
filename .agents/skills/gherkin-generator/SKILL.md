---
name: gherkin-generator
description: "Chuyển đổi User Stories thành bộ kịch bản kiểm thử hành vi (Behavior-Driven Development - BDD) theo chuẩn cú pháp Gherkin (Feature, Scenario, Given, When, Then, And, But) dùng cho PRD, Plan và Pytest/Jest mapping."
---

# Kỹ Năng: Gherkin BDD Generator (Antigravity 2.0)

## 🎯 1. Mục Đích & Phạm Vi Ứng Dụng
Kỹ năng này phục vụ cho:
- **`ba` (Business Analyst)**: Chuyển đổi Acceptance Criteria (AC) dạng văn bản tự do thành các kịch bản kiểm thử hành vi chuẩn Gherkin trong `docs/specs/<feature-slug>/prd.md`.
- **`planner`**: Ánh xạ các kịch bản Gherkin vào Ma Trận Truy Xuất AC Matrix (`FR-xx` -> `BAC-xx` -> `AC-xx` -> `TC-xx`) trong `plan.md`.
- **`qa-tester`**: Dùng các kịch bản Gherkin làm khung tham chiếu 1:1 để viết bài kiểm thử tự động trong Pytest (`test_scenario_xxx`) và Jest/E2E without hallucination.

---

## 📐 2. Cú Pháp Chuẩn Gherkin (BDD Format)

```gherkin
Feature: [Tên tính năng hoặc lát cắt nghiệp vụ - Feature Slug]
  As a [Vai trò người dùng / Persona]
  I want to [Hành động mong muốn thực hiện]
  So that [Mục tiêu kinh doanh hoặc giá trị thu được]

  Background:
    Given [Tiền điều kiện nền tảng áp dụng chung cho mọi kịch bản]

  # --------------------------------------------------------------------------
  # 1. Kịch bản Thành Công (Happy Path)
  # --------------------------------------------------------------------------
  Scenario: [Mã kịch bản SC-01] - [Tên kịch bản thành công]
    Given [Trạng thái hệ thống ban đầu hợp lệ hoặc người dùng đã xác thực]
    When [Người dùng gửi yêu cầu với dữ liệu hợp lệ (POST/GET/PUT/DELETE)]
    Then [Hệ thống phản hồi mã trạng thái HTTP thành công (200 OK / 201 Created)]
    And [Dữ liệu JSON trả về tuân thủ đúng schema snake_case]
    And [Trạng thái trong Cơ sở dữ liệu được cập nhật chính xác]

  # --------------------------------------------------------------------------
  # 2. Kịch bản Ngoại Lệ & Kiểm Soát Lỗi (Edge & Error Paths)
  # --------------------------------------------------------------------------
  Scenario: [Mã kịch bản SC-02] - [Từ chối truy cập khi chưa xác thực]
    Given [Người dùng chưa đăng nhập hoặc token đã hết hạn]
    When [Người dùng cố gắng truy cập tài nguyên bảo mật]
    Then [Hệ thống từ chối với HTTP 401 Unauthorized]
    And [Thông báo lỗi chứa cấu trúc chuẩn: {"detail": "..."}]

  # --------------------------------------------------------------------------
  # 3. Kịch bản Tham Số Hóa (Scenario Outline cho Boundary / Validation)
  # --------------------------------------------------------------------------
  Scenario Outline: [Mã kịch bản SC-03] - [Kiểm tra tính hợp lệ của dữ liệu đầu vào]
    Given [Người dùng đã đăng nhập vào hệ thống]
    When [Người dùng gửi payload có trường <field> mang giá trị <invalid_value>]
    Then [Hệ thống trả về HTTP 422 Unprocessable Entity hoặc HTTP 400 Bad Request]
    And [Chi tiết lỗi chỉ rõ vi phạm tại trường <field>]

    Examples:
      | field       | invalid_value | expected_code |
      | email       | "invalid-mail"| 422           |
      | phone       | "123"         | 422           |
      | quantity    | 0             | 400           |
      | price       | -50000        | 422           |
```

---

## 🛡️ 3. Quy Tắc Bắt Buộc (BDD Guardrails)
1. **Quy tắc 1-Happy + 2-Edge/Error**: Với mỗi User Story chính, BẮT BUỘC phải có ít nhất:
   - 1 Kịch bản Happy Path.
   - Ít nhất 2 Kịch bản Edge/Error (ví dụ: Thiếu quyền hạn 401/403, dữ liệu sai định dạng 422, hoặc xung đột tài nguyên 409).
2. **Quy tắc Định Lượng (Quantitative Assertions)**:
   - TUYỆT ĐỐI KHÔNG dùng câu chữ cảm tính như *"hệ thống xử lý nhanh chóng"*, *"giao diện đẹp mắt"*.
   - BẮT BUỘC viết cụ thể: *"hệ thống trả về HTTP 200 trong vòng 200ms"*, *"hiển thị thẻ Empty State với icon search và nút 'Tạo mới'"*.
3. **Thống Nhất Casing `snake_case`**:
   - Mọi trường dữ liệu được nhắc đến trong kịch bản Gherkin phải dùng đúng định dạng `snake_case` (ví dụ: `order_id`, `created_at`, `total_amount`), tuyệt đối không dùng `camelCase`.
