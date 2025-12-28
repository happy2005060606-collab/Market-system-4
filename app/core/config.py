import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "CRM System"
    API_V1_STR: str = "/api/v1"
    # 默认值适配 GitHub Actions 环境
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:123456@localhost:3306/crm_db")
    ENCRYPTION_ACTIVE_KEYS_JSON: str = '{"key_v1": "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"}'
    ENCRYPTION_CURRENT_KEY_ID: str = "key_v1"
    DEFAULT_TENANT_ID: int = 1

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
