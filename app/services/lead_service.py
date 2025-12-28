import time
import hashlib
from typing import List, Tuple, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, update
from fastapi import HTTPException
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadFilter
from app.core.security import encryption_service

class LeadService:
    def create_lead(self, db: Session, lead_in: LeadCreate, tenant_id: int) -> Lead:
        search_hash = encryption_service.hash_for_search(lead_in.phone)
        exists = db.query(Lead).filter(Lead.tenant_id == tenant_id, Lead.phone_search_hash == search_hash).first()
        if exists:
            raise HTTPException(status_code=409, detail=f"Lead exists with ID {exists.lead_id}")
        
        ciphertext, iv, key_id = encryption_service.encrypt(lead_in.phone)
        db_obj = Lead(
            tenant_id=tenant_id, phone_encrypted=ciphertext, phone_enc_iv=iv,
            phone_enc_key_id=key_id, phone_search_hash=search_hash,
            name=lead_in.name, source=lead_in.source, intention_level=lead_in.intention_level,
            pool_type="public", owner_user_id=None
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_leads(self, db: Session, filters: LeadFilter, tenant_id: int) -> Tuple[List[Lead], int]:
        query = db.query(Lead).filter(Lead.tenant_id == tenant_id)
        if filters.is_new_lead:
            cutoff = datetime.now() - timedelta(days=30)
            query = query.filter(or_(
                and_(Lead.assigned_at.isnot(None), Lead.assigned_at >= cutoff),
                and_(Lead.assigned_at.is_(None), Lead.created_at >= cutoff)
            ))
        if filters.pool_type:
            query = query.filter(Lead.pool_type == filters.pool_type)
        
        total = query.count()
        items = query.order_by(desc(Lead.created_at)).offset((filters.page-1)*filters.page_size).limit(filters.page_size).all()
        return items, total

    def claim_lead(self, db: Session, redis, lead_id: int, user_id: int, tenant_id: int, idempotency_key: Optional[str] = None) -> bool:
        if not idempotency_key:
            bucket = int(time.time() / 10)
            raw = f"{user_id}:{lead_id}:{tenant_id}:{bucket}"
            idempotency_key = hashlib.sha256(raw.encode()).hexdigest()
        
        redis_key = f"claim:{idempotency_key}"
        if redis.get(redis_key): return True

        lead = db.query(Lead).filter(Lead.lead_id == lead_id, Lead.tenant_id == tenant_id).first()
        if not lead: raise HTTPException(status_code=404, detail="Not found")
        if lead.owner_user_id == user_id: return True
        if lead.owner_user_id is not None: raise HTTPException(status_code=409, detail="Owned")

        stmt = update(Lead).where(
            Lead.lead_id == lead_id, Lead.owner_user_id.is_(None), Lead.version == lead.version
        ).values(owner_user_id=user_id, pool_type="private", assigned_at=datetime.now(), version=Lead.version+1)
        
        result = db.execute(stmt)
        db.commit()
        if result.rowcount == 0: raise HTTPException(status_code=409, detail="Conflict")
        
        redis.setex(redis_key, 60, "1")
        return True

lead_service = LeadService()
