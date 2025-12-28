from sqlalchemy import Column, Integer, String, DateTime, BigInteger, JSON, text
from app.core.database import Base

class HandoverBatch(Base):
    __tablename__ = "handover_batch"
    batch_id = Column(BigInteger, primary_key=True, index=True)
    tenant_id = Column(BigInteger, nullable=False, default=1)
    handover_type = Column(String(20), nullable=False)
    from_user_id = Column(BigInteger, nullable=False)
    strategy = Column(String(20), nullable=False)
    filters_snapshot = Column(JSON, nullable=True)
    total_selected = Column(Integer, default=0)
    total_transferred = Column(Integer, default=0)
    status = Column(String(20), nullable=False, default="draft")
    created_by = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

class HandoverItem(Base):
    __tablename__ = "handover_item"
    item_id = Column(BigInteger, primary_key=True, index=True)
    batch_id = Column(BigInteger, nullable=False, index=True)
    lead_id = Column(BigInteger, nullable=False, index=True)
    from_user_id = Column(BigInteger, nullable=False)
    to_user_id = Column(BigInteger, nullable=False)
    result = Column(String(20), nullable=True)
    transferred_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
