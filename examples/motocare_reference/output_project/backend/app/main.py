from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.routers import auth, orders, catalog, health

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Clean Architecture API cho MotoCare_Upgrade"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khởi tạo bảng dữ liệu & thực thi Alembic Migrations
init_db()
try:
    from app.core.migration_manager import run_migrations
    run_migrations()
except Exception:
    pass

# Đăng ký Routers
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(orders.router, prefix=settings.API_V1_STR)
app.include_router(catalog.router, prefix=settings.API_V1_STR)
