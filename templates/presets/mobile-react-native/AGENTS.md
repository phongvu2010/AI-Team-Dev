# Mobile App Layer Rules (`src/mobile/AGENTS.md`)

Quy tắc bắt buộc khi bất kỳ Agent nào (`frontend-dev`, `qa-tester`, `code-reviewer`) thao tác trong thư mục `src/mobile/`:

---

## 1. Rào Chắn An Toàn Dòng Lệnh (CLI Guardrails)
- **Quyền sở hữu File**: Tác tử `frontend-dev` được phép tạo và chỉnh sửa file trong `src/mobile/` khi dự án có phân hệ Mobile. Tuyệt đối không can thiệp vào `src/db/` hay `src/backend/`.
- **Lệnh được phép**:
  - `npm --prefix src/mobile run typecheck`
  - `npm --prefix src/mobile run lint`
  - `npm --prefix src/mobile run start`
- **Lệnh cấm tuyệt đối**:
  - Cấm chạy `npm install` trần trong sandbox; khi cần thêm package (như `expo-camera`, `@gorhom/bottom-sheet`), BẮT BUỘC chỉ cắm cờ `[DEPENDENCY REQUIRED]`.
  - Cấm tự ý sửa `src/mobile/package.json` khi chưa có phê duyệt từ Tech Lead Orchestrator.

---

## 2. Tiêu Chuẩn Kiến Trúc React Native & NativeWind (Tailwind CSS)
1. **Styling qua NativeWind**:
   - Sử dụng thuộc tính `className="..."` với cú pháp Tailwind CSS chuẩn (`flex-1`, `bg-slate-900`, `p-4`, `rounded-2xl`).
   - Hạn chế viết `StyleSheet.create()` thủ công trừ các animation phức tạp.
2. **Components Cốt Lõi**:
   - Dùng `<SafeAreaView>` từ `react-native-safe-area-context` cho top/bottom screens.
   - Dùng `<Pressable>` thay cho `TouchableOpacity`.
   - Dùng `<ScrollView>` hoặc `<FlatList>` cho danh sách dài có phân trang.
3. **Tuân thủ Hợp đồng Dữ liệu (Contract Alignment)**:
   - Các interface trong `src/mobile/src/types/` bắt buộc phải sử dụng chuẩn `snake_case` khớp 100% với `plan.md`. Tuyệt đối không tự ý đổi sang `camelCase`.
   - Mọi response API serialize trực tiếp theo Pydantic model từ Backend.
4. **Xử lý Đủ 4 Trạng Thái UI**:
   - Loading (`ActivityIndicator`), Error (Thông báo kèm nút Retry), Empty (Placeholder kèm CTA), Success (Render dữ liệu).
