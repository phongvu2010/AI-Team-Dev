import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_orders_and_capacity_limit_rule():
    headers = {"Authorization": "Bearer test_valid_token"}
    slot_time = f"2026-10-20T{uuid.uuid4().hex[:4]}:00Z"

    # Đặt các yêu cầu hợp lệ cho tới giới hạn MAX_SLOT_CAPACITY
    max_cap = settings.MAX_SLOT_CAPACITY
    for i in range(max_cap):
        payload = {
            "item_id": f"item_{i}",
            "scheduled_time": slot_time,
            "notes": f"Đơn hàng hợp lệ số {i}"
        }
        resp = client.post("/api/v1/orders", json=payload, headers=headers)
        assert resp.status_code == 201
        assert resp.json()["status"] == "CONFIRMED"

    # Đơn tiếp theo cùng slot_time phải bị từ chối theo BR-01 (400 Bad Request)
    payload_overflow = {
        "item_id": "item_overflow",
        "scheduled_time": slot_time,
        "notes": "Cố tình đặt vượt công suất"
    }
    resp_overflow = client.post("/api/v1/orders", json=payload_overflow, headers=headers)
    assert resp_overflow.status_code == 400
    assert "đạt giới hạn tối đa" in resp_overflow.json()["detail"]

def test_health_check_and_catalog():
    resp_health = client.get("/api/v1/health")
    assert resp_health.status_code == 200
    assert resp_health.json()["status"] == "healthy"

    resp_cat = client.get("/api/v1/catalog")
    assert resp_cat.status_code == 200
    assert isinstance(resp_cat.json(), list)
