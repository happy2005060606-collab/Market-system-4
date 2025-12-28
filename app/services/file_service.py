from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.file_object import FileObject
import hashlib, os

class FileService:
    def upload_file(self, db: Session, file, file_class: str, user_id: int, tenant_id: int):
        content = file.file.read()
        sha256 = hashlib.sha256(content).hexdigest()
        path = f"{tenant_id}/{sha256}"
        # Mock save
        db_file = FileObject(
            tenant_id=tenant_id, file_class=file_class, storage_path=path,
            sha256_hash=sha256, uploaded_by=user_id, is_deleted=0
        )
        db.add(db_file)
        db.commit()
        return db_file

    def soft_delete_file(self, db: Session, file_id: int):
        f = db.query(FileObject).filter(FileObject.file_id == file_id).first()
        if not f: raise HTTPException(404, "Not found")
        if f.file_class.startswith("EVIDENCE"): raise HTTPException(403, "WORM Protected")
        f.is_deleted = 1
        db.commit()
        return {"status": "deleted"}

file_service = FileService()
