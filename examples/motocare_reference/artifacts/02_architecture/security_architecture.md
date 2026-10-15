# BẢO MẬT HỆ THỐNG & MÔ HÌNH STRIDE
**Dự án:** MotoCare_Upgrade

## 1. MA TRẬN PHÒNG VỆ NGUY CƠ (STRIDE MATRIX)

| Mối Đe Dọa (STRIDE) | Biện Pháp Phòng Vệ Kỹ Thuật |
|---|---|
| **Spoofing (Giả mạo)** | Xác thực JWT HS256, hash mật khẩu Bcrypt với salt cost 12. |
| **Tampering (Sửa đổi dữ liệu)** | Pydantic DTOs validate kiểu dữ liệu chặt chẽ; HTTPS bắt buộc. |
| **Information Disclosure** | Ẩn chi tiết stack trace ở production; lọc trường nhạy cảm trong Response DTO. |
| **Denial of Service** | Áp dụng quy tắc kiểm soát công suất (Giới hạn tối đa 3 xe mỗi khung giờ (BR-01)) và rate limiting. |
