# ==============================================================================
# FastAPI Backend Production Dockerfile (`src/backend/Dockerfile`)
# Multi-Agent Dev Team — Antigravity 2.0
# ==============================================================================
FROM python:3.12-slim AS runner

# Prevent Python from writing .pyc files & enable unbuffered terminal logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# Install system dependencies (curl for container healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create dedicated non-root user and group for security (OWASP compliance)
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -s /bin/bash -m appuser

# Install Python dependencies first to leverage Docker layer caching
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Copy application source code (src/db and src/backend)
COPY src/ /app/src/

# Set ownership of the application directory to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose backend service port
EXPOSE 8000

# Periodic container healthcheck against FastAPI health endpoints
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start Uvicorn ASGI server
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
