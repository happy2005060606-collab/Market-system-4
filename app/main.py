from fastapi import FastAPI
from app.core.config import get_settings
from app.middleware.tenant import TenantMiddleware
from app.api.api import api_router

settings = get_settings()
app = FastAPI(title=settings.PROJECT_NAME)
app.add_middleware(TenantMiddleware)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health(): return {"status": "ok"}
