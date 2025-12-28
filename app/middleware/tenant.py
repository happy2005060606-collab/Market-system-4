from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from contextvars import ContextVar
from app.core.config import get_settings

settings = get_settings()
tenant_context: ContextVar[int] = ContextVar("tenant_id", default=settings.DEFAULT_TENANT_ID)

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tid = request.headers.get("X-Tenant-ID")
        token = tenant_context.set(int(tid) if tid and tid.isdigit() else settings.DEFAULT_TENANT_ID)
        try: return await call_next(request)
        finally: tenant_context.reset(token)

def get_current_tenant_id() -> int:
    return tenant_context.get()
