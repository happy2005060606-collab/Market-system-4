from sqlalchemy import Column, Integer, String, DateTime, text, LargeBinary, BigInteger
from sqlalchemy.dialects.mysql import TINYINT, CHAR
from app.core.database import Base

class Lead(Base):
    __tablename__ = "lead"
    lead_id = Column(BigInteger, primary_key=True, index=True)
    tenant_id = Column(BigInteger, nullable=False, default=1)
    phone_encrypted = Column(LargeBinary(128), nullable=False)
    phone_enc_iv = Column(LargeBinary(24), nullable=False)
    phone_enc_key_id = Column(String(64), nullable=False)
    phone_search_hash = Column(CHAR(64), nullable=False)
    pool_type = Column(String(20), nullable=False)
    owner_user_id = Column(BigInteger, nullable=True)
    status = Column(String(20), nullable=False, default="new")
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    assigned_at = Column(DateTime, nullable=True)
    first_contact_at = Column(DateTime, nullable=True)
    last_contact_at = Column(DateTime, nullable=True)
    next_followup_time = Column(DateTime, nullable=True)
    invalid_flag = Column(TINYINT(1), default=0)
    version = Column(Integer, default=1, nullable=False)
