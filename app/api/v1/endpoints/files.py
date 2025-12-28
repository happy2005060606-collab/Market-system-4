from fastapi import APIRouter, Depends, UploadFile, Form
from sqlalchemy.orm import Session
from app.api import deps
from app.services.file_service import file_service

router = APIRouter()

@router.post("/upload")
def upload(file: UploadFile, file_class: str = Form(...), db: Session = Depends(deps.get_db), tid: int = Depends(deps.get_tenant_id), uid: int = Depends(deps.get_current_user_id)):
    obj = file_service.upload_file(db, file, file_class, uid, tid)
    return {"file_id": obj.file_id}

@router.delete("/{file_id}")
def delete(file_id: int, db: Session = Depends(deps.get_db), uid: int = Depends(deps.get_current_user_id)):
    return file_service.soft_delete_file(db, file_id, uid)
