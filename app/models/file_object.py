from sqlalchemy import Column, String, BigInteger, DateTime, text
from sqlalchemy.dialects.mysql import TINYINT, CHAR
from app.core.database import Base

class FileObject(Base):
    __tablename__ = "file_object"
    file_id = Column(BigInteger, primary_key=True, index=True)
    tenant_id = Column(BigInteger, nullable=False, default=1)
    file_class = Column(String(20), nullable=False)
    storage_path = Column(String(500), nullable=False)
    sha256_hash = Column(CHAR(64), nullable=False)
    uploaded_by = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    is_deleted = Column(TINYINT(1), default=0)
