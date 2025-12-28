from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.lead import LeadCreate, LeadResponse, LeadFilter
from app.services.lead_service import lead_service
from app.core.security import encryption_service

router = APIRouter()

@router.post("/", response_model=LeadResponse)
def create_lead(lead_in: LeadCreate, db: Session = Depends(deps.get_db), tenant_id: int = Depends(deps.get_tenant_id)):
    lead = lead_service.create_lead(db, lead_in, tenant_id)
    resp = LeadResponse.model_validate(lead)
    resp.phone_masked = encryption_service.mask_phone(lead_in.phone)
    return resp

@router.post("/list")
def list_leads(filters: LeadFilter, db: Session = Depends(deps.get_db), tenant_id: int = Depends(deps.get_tenant_id)):
    items, total = lead_service.get_leads(db, filters, tenant_id)
    return {"total": total, "items": items}

@router.post("/{lead_id}/claim")
def claim_lead(lead_id: int, db: Session = Depends(deps.get_db), redis=Depends(deps.get_redis), 
               uid: int = Depends(deps.get_current_user_id), tid: int = Depends(deps.get_tenant_id),
               idem_key: str = Header(None, alias="X-Idempotency-Key")):
    lead_service.claim_lead(db, redis, lead_id, uid, tid, idem_key)
    return {"status": "success"}
