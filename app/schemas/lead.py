from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LeadCreate(BaseModel):
    name: Optional[str] = None
    phone: str = Field(..., min_length=11)
    source: Optional[str] = None
    intention_level: Optional[int] = None

class LeadFilter(BaseModel):
    is_new_lead: bool = False
    pool_type: Optional[str] = None
    page: int = 1
    page_size: int = 20

class LeadResponse(LeadCreate):
    lead_id: int
    tenant_id: int
    phone_masked: str
    pool_type: str
    owner_user_id: Optional[int]
    status: str
    created_at: datetime
    assigned_at: Optional[datetime]
    class Config:
        from_attributes = True
