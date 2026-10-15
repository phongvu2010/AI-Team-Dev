---
name: secret-scanner
description: "Quét tĩnh mã nguồn để phát hiện rò rỉ khóa bí mật, API Keys, mật khẩu cơ sở dữ liệu, private keys và tokens thông qua entropy analysis và regex patterns."
---

# Secret Scanner & Credential Leak Prevention Skill

## Mục đích
Hỗ trợ **Principal Code Reviewer (`code-reviewer`)** và **QA Tester (`qa-tester`)** phát hiện và ngăn chặn nguy cơ rò rỉ thông tin nhạy cảm, mật khẩu hoặc khóa bí mật trong mã nguồn `src/` trước khi đóng gói commit vào kho lưu trữ.

---

## 1. Danh Mục Các Mẫu Nhận Diện Nguy Cơ Cao (High-Risk Patterns)

| Loại Bí Mật | Mẫu Regex / Dấu Hiệu Nhận Diện | Hành Động Khắc Phục Bắt Buộc |
| :--- | :--- | :--- |
| **Database Connection String** | `(?:postgresql|postgres|mysql|mongodb)\+?[a-z]*:\/\/[^:]+:[^@]+@` | Di chuyển vào biến môi trường `DATABASE_URL` trong `.env`. |
| **API Keys & Secret Tokens** | `(?i)(?:api_key|secret_key|jwt_secret|auth_token)\s*=\s*['"][a-zA-Z0-9_\-\.]{16,}['"]` | Đọc qua Pydantic Settings (`pydantic-settings`) hoặc `os.getenv()`. |
| **OpenAI / Anthropic Keys** | `(?:sk-[a-zA-Z0-9]{20,}|sk-ant-[a-zA-Z0-9]{20,})` | Đưa vào `.env`, cấm commit source code. |
| **Google API Keys** | `AIza[0-9A-Za-z\-_]{35}` | Đưa vào `.env`. |
| **GitHub Personal Tokens** | `(?:ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36}` | Thu hồi token ngay lập tức và đưa vào `.env`. |
| **Private Keys & Certificates** | `-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----` | Lưu vào file pem riêng được khai báo trong `.gitignore` hoặc nạp qua Secret Vault. |
| **Webhooks with Credentials** | `https:\/\/(?:discord\.com\/api\/webhooks|hooks\.slack\.com\/services)\/[a-zA-Z0-9_\-\/]+` | Nạp URL webhook từ `.env`. |

---

## 2. Quy Trình Rà Soát Dành Cho Code Reviewer

Khi thực hiện audit qua `git diff`:
1. **Quét Diff Thay Đổi**:
   Kiểm tra toàn bộ các dòng thêm mới (`+`) trong `git diff`. Nếu phát hiện bất kỳ chuỗi ký tự nào khớp với danh mục trên:
2. **Gắn Cờ Vi Phạm Nghiêm Trọng (`[CRITICAL]`)**:
   - Phân loại: `Security / Zero Hardcoded Secrets`.
   - Mức độ: `CRITICAL`.
   - Kết luận (Verdict): Tự động đánh giá **`CHANGES_REQUESTED`** (tuyệt đối không cấp phép `APPROVED`).
3. **Hướng Dẫn Khắc Phục**:
   - Chỉ rõ file và số dòng vi phạm.
   - Yêu cầu Dev Squad khai báo biến trong `.env.example` (với giá trị placeholder) và nạp qua cấu hình hệ thống:
     ```python
     # Vi phạm:
     SECRET_KEY = "my-super-secret-jwt-key"

     # Chuẩn mực:
     from pydantic_settings import BaseSettings

     class Settings(BaseSettings):
         SECRET_KEY: str
         DATABASE_URL: str
         
         model_config = ConfigDict(env_file=".env", extra="ignore")
     ```
