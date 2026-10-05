---
name: ba-requirements
description: >-
  Business analysis, requirements elicitation, interactive interview techniques, user journey mapping, and PRD specification patterns for the BA Agent (ba). Activate when clarifying user prompts, identifying business rules and edge cases, interviewing users via interactive questions, or writing Product Requirements Documents (PRD) in docs/specs/<feature-slug>/prd.md.
---

# Business Analysis & Requirements Engineering Runbook (`ba-requirements`)

Runbook này hướng dẫn **BA Agent (`ba`)** phương pháp làm rõ yêu cầu nghiệp vụ, kỹ thuật phỏng vấn người dùng có cấu trúc qua công cụ `ask_question`, phát hiện kịch bản ngoại lệ (Edge Cases), thiết lập quy tắc nghiệp vụ (Business Rules), và xuất bản tài liệu **Product Requirements Document (PRD)** chuẩn hóa tại `docs/specs/<feature-slug>/prd.md`.

---

## 1. Phân Định Trách Nhiệm: BA (`ba`) vs Planner (`planner`)

Để tránh chồng chéo nhiệm vụ và đảm bảo tính mạch lạc xuyên suốt pipeline:

| Tiêu chí | BA Agent (`ba`) | Technical Planner (`planner`) |
| :--- | :--- | :--- |
| **Câu hỏi cốt lõi** | **WHAT & WHY**: Tính năng này giải quyết vấn đề gì? Ai dùng? Quy tắc nghiệp vụ ra sao? | **HOW**: Hệ thống cài đặt như thế nào? Bảng DB nào? API schema nào? Component nào? |
| **Đối tượng phỏng vấn** | Phỏng vấn trực tiếp Người dùng (End User / Product Owner) qua `ask_question`. | Tra cứu PRD và khảo sát codebase kỹ thuật, không làm phiền người dùng về tiểu tiết. |
| **Đầu vào (Input)** | Prompt / Yêu cầu ban đầu từ người dùng (thường mơ hồ, ngắn gọn, thiếu edge cases). | Tài liệu PRD (`docs/specs/<feature-slug>/prd.md`) đã được người dùng nghiệm thu. |
| **Sản phẩm bàn giao** | `docs/specs/<feature-slug>/prd.md` (FRs, BRs, Personas, User Journeys, Edge Cases, BACs). | `docs/specs/<feature-slug>/plan.md` (Cross-layer Data Matrix, API Spec, UI Spec, AC/TC Matrix). |
| **Ranh giới cấm** | Không quyết định tên cột DB, cú pháp code, thư viện kỹ thuật. | Không tự ý thay đổi quy tắc nghiệp vụ hoặc phạm vi đã chốt trong PRD. |

---

## 2. Kỹ Thuật Phỏng Vấn & Làm Rõ Yêu Cầu (Requirements Elicitation Protocol)

Khi tiếp nhận prompt từ người dùng, BA Agent tuyệt đối **không được giả định ngầm** những điểm mấu chốt mà phải sử dụng công cụ `ask_question` để phỏng vấn:

### 2.1. Ma Trận Phát Hiện Điểm Mù Nghiệp Vụ (Blind Spot Matrix)
1. **Scope Boundary (Phạm vi ranh giới)**:
   - *Vấn đề*: Người dùng yêu cầu "Làm tính năng quản lý sản phẩm".
   - *Cần làm rõ*: MVP có bao gồm quản lý kho, nhập hàng, biến thể sản phẩm (màu sắc, kích cỡ) không, hay chỉ là CRUD sản phẩm cơ bản?
2. **Actor & Permission (Tác nhân & Quyền hạn)**:
   - *Vấn đề*: "Người dùng có thể xóa bài viết".
   - *Cần làm rõ*: Bất kỳ người dùng nào hay chỉ tác giả của bài viết? Admin có quyền xóa không? Có cơ chế Soft Delete (thùng rác) để phục hồi không?
3. **Data Constraints & Business Rules (Ràng buộc dữ liệu & Quy tắc)**:
   - *Vấn đề*: "Người dùng nhập mã giảm giá".
   - *Cần làm rõ*: Mã giảm giá có phân biệt hoa/thường không? Một đơn hàng áp dụng tối đa bao nhiêu mã? Có áp dụng đồng thời với khuyến mãi khác không?
4. **Edge Cases & Failure Behavior (Hành vi khi có lỗi)**:
   - *Vấn đề*: Người dùng bấm lưu dữ liệu khi mất mạng hoặc server chậm.
   - *Cần làm rõ*: Hệ thống hiển thị cảnh báo gì? Có tự động lưu bản nháp vào LocalStorage không? Có cơ chế Retry không?

### 2.2. Quy Tắc Phỏng Vấn Tối Ưu Với `ask_question` (High-Leverage Interview Protocol)
- **Giới hạn số lượng (Hard Limit)**: Chỉ hỏi tối đa **1 đến 3 câu hỏi cốt lõi nhất (P0)** trong toàn bộ phiên phỏng vấn. Chỉ hỏi về các quyết định mang tính chiến lược: phạm vi MVP, đối tượng/quyền hạn người dùng, hoặc quy tắc nghiệp vụ rẽ nhánh chính.
- **Cấu trúc phương án**: Luôn gom thành câu hỏi trắc nghiệm kèm mô tả trực quan, gắn tiền tố `(Recommended)` cho phương án tối ưu theo best practice để người dùng dễ dàng bấm chọn.
- **Nguyên tắc Phân tách Nghiệp vụ vs Tiểu tiết (Separation of Concerns)**:
  - Tuyệt đối KHÔNG hỏi các chi tiết thứ yếu (P1/P2, giao diện màu sắc/icon, edge cases kỹ thuật, tên trường dữ liệu).
  - Đối với các điểm này, BA chủ động đưa ra giải pháp khuyến nghị hợp lý nhất và trình bày rõ ràng trong Mục 3, Mục 5 và Mục 6 của tài liệu `prd.md`.
  - Người dùng sẽ nghiệm thu toàn diện các đề xuất này một lần duy nhất tại **Cổng Nghiệm Thu PRD (PRD Sign-off Gate)**, tránh bị gián đoạn nhiều lần.

---

## 3. Tiêu Chuẩn Soạn Thảo PRD (`docs/specs/<feature-slug>/prd.md`)

Tài liệu PRD phải tuân thủ nghiêm ngặt mẫu [prd-template.md](../team-pipeline/resources/prd-template.md):

### 3.1. Cấu trúc Metadata Header
```yaml
---
feature_slug: "<feature-slug>"
version: "1.0.0"
artifact_type: "prd"
author: "ba"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
status: "DRAFT" # DRAFT -> PENDING_REVIEW -> APPROVED_BY_USER
iteration: 1
---
```

### 3.2. Tiêu Chuẩn Viết Yêu Cầu Chức Năng (Functional Requirements - FRs)
- Đặt mã định danh duy nhất: `FR-01`, `FR-02`, `FR-03`...
- Mỗi FR phải độc lập, kiểm thử được và nêu rõ hành vi hệ thống:
  - *Ví dụ tốt*: `FR-01: Hệ thống cho phép người dùng lọc danh sách giao dịch theo khoảng ngày (Từ ngày - Đến ngày) với kết quả cập nhật theo thời gian thực.`
  - *Ví dụ xấu*: `FR-01: Làm bộ lọc xịn sò.`

### 3.3. Tiêu Chuẩn Viết Tiêu Chí Nghiệm Thu Nghiệp Vụ (Business Acceptance Criteria - BACs)
Áp dụng cấu trúc **Given - When - Then** chuẩn Agile:
```markdown
### BAC-01: Xác thực mã giảm giá hợp lệ
- **Given**: Người dùng đã thêm sản phẩm vào giỏ hàng với tổng giá trị đạt tối thiểu 200,000 VNĐ.
- **When**: Người dùng nhập mã "GIAM50K" và bấm "Áp dụng".
- **Then**: Hệ thống trừ 50,000 VNĐ vào tổng thanh toán, hiển thị nhãn xanh "Đã áp dụng mã GIAM50K", và cập nhật số tiền cần trả.
```

---

## 4. Quy Trình Phê Duyệt & Bàn Giao (PRD Sign-off Gate)

1. **Soạn thảo xong bản thảo PRD**: Thiết lập `status: "DRAFT"`.
2. **Trình bày tóm tắt cho User**: Tóm lược phạm vi In-Scope, Out-of-Scope, Business Rules chính và các BACs.
3. **Xin xác nhận Sign-off**: Sử dụng `ask_question` hoặc tương tác trực tiếp với User để lấy xác nhận: "Bạn có đồng ý với bản PRD này để chuyển sang giai đoạn thiết kế kỹ thuật (Planning) không?".
4. **Cập nhật trạng thái**: Khi User đồng ý, cập nhật `status: "APPROVED_BY_USER"`.
5. **Kích hoạt Phase 1**: Thông báo cho Tech Lead Orchestrator chuyển giao `docs/specs/<feature-slug>/prd.md` cho `planner`.
