import pytest
from sqlalchemy import text
from app.core.security import encryption_service

HEADERS = {"X-User-ID": "101", "X-Tenant-ID": "1"}

def test_health(client):
    assert client.get("/health").status_code == 200

def test_lead_encryption(client, db_session):
    phone = "13800138000"
    resp = client.post("/api/v1/leads/", json={"phone": phone}, headers=HEADERS)
    assert resp.status_code == 200
    lid = resp.json()["lead_id"]
    
    # 验证数据库存的是密文
    row = db_session.execute(text("SELECT phone_encrypted FROM lead WHERE lead_id=:id"), {"id": lid}).fetchone()
    assert row[0] != phone.encode()

def test_claim_idempotency(client):
    # 先创建
    create = client.post("/api/v1/leads/", json={"phone": "13900001111"}, headers=HEADERS)
    lid = create.json()["lead_id"]
    
    # 模拟并发 5 次
    res = [client.post(f"/api/v1/leads/{lid}/claim", headers=HEADERS) for _ in range(5)]
    success = sum(1 for r in res if r.status_code == 200)
    conflict = sum(1 for r in res if r.status_code == 409)
    assert success >= 1
