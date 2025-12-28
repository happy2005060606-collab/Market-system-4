from typing import Generator
from fastapi import Header
import redis
from app.core.database import SessionLocal
from app.middleware.tenant import get_current_tenant_id

redis_pool = redis.ConnectionPool.from_url("redis://localhost:6379/0", decode_responses=True)

def get_db() -> Generator:
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_redis() -> redis.Redis:
    return redis.Redis(connection_pool=redis_pool)

def get_current_user_id(x_user_id: str = Header("1", alias="X-User-ID")) -> int:
    return int(x_user_id)

def get_tenant_id() -> int:
    return get_current_tenant_id()
