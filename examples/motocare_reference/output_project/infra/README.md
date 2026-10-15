# Hạ Tầng Container & Triển Khai (MotoCare)

Tài liệu hướng dẫn triển khai hệ thống phân tán đa container sử dụng **Multi-Stage Dockerfile** cho cả Frontend và Backend.

---

## 🏗️ Kiến Trúc Multi-Stage Dockerfile

### 1. Frontend Web & Mobile Preview (`infra/Dockerfile.frontend`):
- **Stage 1 (Builder):** `node:20-alpine` cài đặt dependencies, biên dịch TypeScript và đóng gói Vite/SPA thành static assets.
- **Stage 2 (Runner):** `nginx:1.27-alpine` siêu nhẹ (< 25MB), cấu hình SPA routing fallback (`index.html`), nén Gzip, OWASP Security Headers và reverse proxy trực tiếp các truy vấn `/api/` tới FastAPI.

### 2. Backend API (`infra/Dockerfile.backend` & `infra/Dockerfile`):
- **Stage 1 (Builder):** `python:3.12-slim` cài đặt dependencies qua `--user` flag.
- **Stage 2 (Runner):** Tách biệt runtime, copy packages sang môi trường thực thi sạch, expose cổng `8000` kèm Healthcheck tự động.

### 3. Cơ Sở Dữ Liệu (`db`):
- `postgres:15-alpine` cấu hình healthcheck định kỳ và volume lưu trữ bền vững `pgdata`.

---

## 🚀 Hướng Dẫn Vận Hành

```bash
# Đóng gói toàn bộ images (Frontend Multi-stage + Backend):
docker compose -f infra/docker-compose.yml build

# Khởi chạy toàn bộ hệ sinh thái ngầm:
docker compose -f infra/docker-compose.yml up -d

# Xem log các dịch vụ:
docker compose -f infra/docker-compose.yml logs -f

# Dừng và dọn dẹp containers:
docker compose -f infra/docker-compose.yml down
```
