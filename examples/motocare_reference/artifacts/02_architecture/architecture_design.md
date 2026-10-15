# TÀI LIỆU THIẾT KẾ KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)
**Dự án:** MotoCare_Upgrade
**Phiên bản:** 1.0.0 (Release Candidate)
**Trưởng ban Kiến trúc:** System Architect Agent & Tech Lead

---

## 1. QUYẾT ĐỊNH CÔNG NGHỆ (ARCHITECTURE DECISION RECORDS - ADR)
### ADR-01: Lựa chọn Tech Stack thân thiện với Tech Lead Review
- **Bối cảnh:** Dự án cần phát triển nhanh, chất lượng cao và Tech Lead có thể tự tay review từng file code.
- **Quyết định:** Sử dụng FastAPI (Backend) + React Native (Mobile) + PostgreSQL.
- **Lợi ích:** Mã nguồn dễ bảo trì, typing chặt chẽ, ngăn ngừa lỗi runtime.

### ADR-02: Áp dụng kiến trúc Clean Architecture phân tầng
- **Bối cảnh:** Tránh việc logic nghiệp vụ bị phân tán hoặc lẫn lộn vào tầng Controller/Router.
- **Quyết định:** Chia rõ: Routers -> Services -> Repositories -> Models.
- **Lợi ích:** Dễ viết Unit Test, cô lập lỗi và có thể tráo đổi database mà không ảnh hưởng use case.

---

## 2. TECH STACK ĐÃ CHỌN (PHÙ HỢP TECH LEAD PROFILE)
- **Backend:** Python (FastAPI v0.110+)
- **ORM / Database Access:** SQLAlchemy 2.0 (Async) + Alembic
- **Data Validation:** Pydantic v2.6+
- **Frontend / Mobile:** React Native (TypeScript) + React Navigation
- **Database:** PostgreSQL 15+
- **Caching:** Redis 7.0+
- **Lý do lựa chọn:**
1. Ưu tiên tuyệt đối theo sở trường của Tech Lead: Python/FastAPI và React Native/TypeScript.
2. FastAPI cho hiệu năng IO bất đồng bộ xuất sắc, sinh OpenAPI docs tự động từ Pydantic.
3. PostgreSQL 15+ đảm bảo toàn vẹn dữ liệu ACID và bảo vệ giao dịch đặt hàng.

---

## 3. MÔ HÌNH KIẾN TRÚC PHÂN TẦNG (CLEAN ARCHITECTURE)

```text
               [ Client App (React Native / Next.js) ]
                              │
                              ▼ (HTTPS RESTful)
   ┌─────────────────────────────────────────────────────────┐
   │                 FastAPI Application Server              │
   │  ┌───────────────────────────────────────────────────┐  │
   │  │ 1. API Routing & Controller Layer (Pydantic DTO)  │  │
   │  └─────────────────────────┬─────────────────────────┘  │
   │                            ▼                            │
   │  ┌───────────────────────────────────────────────────┐  │
   │  │ 2. Business Logic / Service Layer (Use Cases)     │  │
   │  └─────────────────────────┬─────────────────────────┘  │
   │                            ▼                            │
   │  ┌───────────────────────────────────────────────────┐  │
   │  │ 3. Data Access / Repository Layer (Async ORM)     │  │
   │  └─────────────────────────┬─────────────────────────┘  │
   └────────────────────────────┼────────────────────────────┘
                                ▼
                     [ PostgreSQL 15+ ]
```
