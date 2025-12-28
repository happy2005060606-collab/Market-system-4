from sqlalchemy.orm import Session
from sqlalchemy import update
from app.models.lead import Lead
from app.models.handover import HandoverBatch, HandoverItem
from app.schemas.handover import HandoverCreate

class HandoverService:
    def create_and_execute(self, db: Session, data: HandoverCreate, operator_id: int, tenant_id: int):
        batch = HandoverBatch(
            tenant_id=tenant_id, handover_type="LEAD_TRANSFER", from_user_id=data.from_user_id,
            strategy=data.strategy, status="executing", created_by=operator_id
        )
        db.add(batch)
        db.flush()
        
        leads = db.query(Lead).filter(
            Lead.tenant_id == tenant_id, Lead.owner_user_id == data.from_user_id, Lead.pool_type == 'private'
        ).limit(1000).all()
        
        success = 0
        for lead in leads:
            item = HandoverItem(
                batch_id=batch.batch_id, lead_id=lead.lead_id,
                from_user_id=data.from_user_id, to_user_id=data.to_user_id, result="success"
            )
            db.add(item)
            lead.owner_user_id = data.to_user_id
            lead.version += 1
            success += 1
            
        batch.total_transferred = success
        batch.status = "executed"
        db.commit()
        db.refresh(batch)
        return batch

    def rollback_batch(self, db: Session, batch_id: int, tenant_id: int):
        batch = db.query(HandoverBatch).filter(HandoverBatch.batch_id==batch_id).first()
        if not batch or batch.status != "executed": raise ValueError("Invalid batch")
        
        items = db.query(HandoverItem).filter(HandoverItem.batch_id == batch_id).all()
        stats = {"total": len(items), "success": 0, "skipped": 0, "skipped_details": []}
        
        for item in items:
            stmt = update(Lead).where(
                Lead.lead_id == item.lead_id, Lead.owner_user_id == item.to_user_id
            ).values(owner_user_id=item.from_user_id, version=Lead.version+1)
            
            res = db.execute(stmt)
            if res.rowcount == 1:
                stats["success"] += 1
            else:
                stats["skipped"] += 1
                stats["skipped_details"].append({"lead_id": item.lead_id, "reason": "CAS_FAIL"})
        
        batch.status = "rollback"
        db.commit()
        return stats

handover_service = HandoverService()
