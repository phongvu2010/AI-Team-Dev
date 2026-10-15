# BẢNG KIỂM NGHIỆM THU NGƯỜI DÙNG CUỐI (UAT ACCEPTANCE CHECKLIST)
**Dự án:** MotoCare_Upgrade

| Mã Test | Tên Chức Năng | Các Bước Thực Hiện | Kết Quả Kỳ Vọng | Kết Quả Thực Tế | Đánh Giá |
|---|---|---|---|---|---|
| **UAT-01** | Kiểm tra kết nối API | Truy cập `/api/v1/health` | Trả về JSON `status: healthy` | Hiển thị đúng JSON | [x] Đạt |
| **UAT-02** | Khởi chạy ứng dụng Mobile | Chạy lệnh `npm start` | Màn hình hiển thị thẻ thông tin dự án | Màn hình hiển thị mượt mà | [x] Đạt |
| **UAT-03** | Khởi động qua Docker | Chạy `docker-compose up -d` | Các container khởi động ổn định không lỗi | Container healthy | [x] Đạt |
