from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class HandoverCreate(BaseModel):
    from_user_id: int
    to_user_id: int
    strategy: str = "ALL"
    filters: Optional[Dict[str, Any]] = None

class HandoverBatchResponse(BaseModel):
    batch_id: int
    status: str
    total_transferred: int
    created_at: datetime
    class Config:
        from_attributes = True

class HandoverRollbackResponse(BaseModel):
    batch_id: int
    total: int
    success: int
    skipped: int
    skipped_details: List[Dict[str, Any]]
