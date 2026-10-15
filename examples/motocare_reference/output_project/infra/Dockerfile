# ==============================================================================
# BACKEND MULTI-STAGE DOCKERFILE (Python 3.12-slim / FastAPI)
# ==============================================================================
FROM python:3.12-slim AS builder
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim AS runner
WORKDIR /app
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
COPY --from=builder /root/.local /root/.local
COPY backend /app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
