from fastapi import APIRouter
from app.api.v1.endpoints import leads, handover, files

api_router = APIRouter()
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(handover.router, prefix="/handover", tags=["handover"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
