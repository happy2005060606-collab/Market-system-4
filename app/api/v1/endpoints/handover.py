from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.handover import HandoverCreate, HandoverBatchResponse, HandoverRollbackResponse
from app.services.handover_service import handover_service

router = APIRouter()

@router.post("/execute", response_model=HandoverBatchResponse)
def execute(data: HandoverCreate, db: Session = Depends(deps.get_db), tid: int = Depends(deps.get_tenant_id), uid: int = Depends(deps.get_current_user_id)):
    return handover_service.create_and_execute(db, data, uid, tid)

@router.post("/{batch_id}/rollback", response_model=HandoverRollbackResponse)
def rollback(batch_id: int, db: Session = Depends(deps.get_db), tid: int = Depends(deps.get_tenant_id)):
    res = handover_service.rollback_batch(db, batch_id, tid)
    return HandoverRollbackResponse(batch_id=batch_id, **res)
