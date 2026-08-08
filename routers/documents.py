from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import date
from pydantic import BaseModel
import models
from database import get_db
from auth import get_current_user, check_employee_access
from typing import List
import os
from pathlib import Path
import shutil

router = APIRouter(prefix="/api/documents", tags=["documents"])
WORD_DOCS_DIR = Path("uploads/word_documents")
WORD_DOCS_DIR.mkdir(parents=True, exist_ok=True)

class DocumentCreate(BaseModel):
    employee_id: int
    document_type: str
    file_path: str

class DocumentResponse(BaseModel):
    id: int
    employee_id: int
    document_type: str
    created_at: date
    class Config:
        from_attributes = True

@router.post("/upload")
async def upload_doc(employee_id: int, document_type: str, file: UploadFile = File(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if current_user.role == "staff" and current_user.employee_id != employee_id:
        raise HTTPException(status_code=403, detail="Staff can only upload documents for themselves")
    if current_user.role == "project_manager" and not check_employee_access(current_user, employee_id, db):
        raise HTTPException(status_code=403, detail="Insufficient permissions to upload documents for this employee")
    if current_user.role not in ("staff", "hr_admin", "project_manager"):
        raise HTTPException(status_code=403, detail="Insufficient permissions to upload documents")

    upload_root = Path("uploads")
    dest_dir = upload_root / str(employee_id)
    dest_dir.mkdir(parents=True, exist_ok=True)
    safe_filename = f"{document_type}_{file.filename}"
    dest_path = dest_dir / safe_filename
    try:
        with dest_path.open("wb") as out_file:
            shutil.copyfileobj(file.file, out_file)
    finally:
        file.file.close()

    # Optionally record audit or link into Employee record (not implemented here)
    return {"message": f"Document {document_type} uploaded successfully", "path": str(dest_path)}


@router.post("/word-documents/bulk-upload")
async def bulk_upload_word_documents(files: List[UploadFile] = File(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role not in {"hr_admin", "project_manager", "staff", "finance"}:
        raise HTTPException(status_code=403, detail="Insufficient permissions to upload Word documents")

    if not files:
        raise HTTPException(status_code=400, detail="No Word documents were provided")

    uploaded = []
    for file in files:
        filename = Path(file.filename or "").name
        if not filename.lower().endswith((".doc", ".docx")):
            continue

        target = WORD_DOCS_DIR / filename
        with target.open("wb") as out_file:
            shutil.copyfileobj(file.file, out_file)

        db.add(models.Notification(
            user_id=current_user.id,
            message=f"Word document '{filename}' was uploaded to the department word-document repository.",
            type="word_document_upload",
            read=False,
        ))
        uploaded.append({"name": filename, "path": str(target)})

    db.commit()
    return {"success": True, "uploaded": uploaded, "message": f"Uploaded {len(uploaded)} Word document(s)"}


@router.get("/word-documents")
def list_word_documents(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role not in {"hr_admin", "project_manager", "staff", "finance"}:
        raise HTTPException(status_code=403, detail="Insufficient permissions to list Word documents")

    documents = []
    for path in sorted(WORD_DOCS_DIR.iterdir()):
        if path.is_file() and path.suffix.lower() in {".doc", ".docx"}:
            documents.append({"name": path.name, "path": str(path)})
    return {"documents": documents}


@router.get("/word-documents/download")
def download_word_document(file_name: str, current_user=Depends(get_current_user)):
    if current_user.role not in {"hr_admin", "project_manager", "staff", "finance"}:
        raise HTTPException(status_code=403, detail="Insufficient permissions to download Word documents")

    target = WORD_DOCS_DIR / file_name
    if not target.exists():
        raise HTTPException(status_code=404, detail="Document not found")
    return FileResponse(target, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=target.name)


@router.post("/word-documents/send")
def send_word_document(payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role not in {"hr_admin", "project_manager", "staff", "finance"}:
        raise HTTPException(status_code=403, detail="Insufficient permissions to send Word documents")

    document_name = payload.get("document_name") or "Unknown document"
    department = payload.get("department") or "general"

    db.add(models.Notification(
        user_id=current_user.id,
        message=f"Word document '{document_name}' has been sent to the {department} department for review.",
        type="word_document_sent",
        read=False,
    ))
    db.commit()

    return {"success": True, "sent_to": department, "document_name": document_name, "message": f"Document sent to {department}"}


@router.get("/employee/{employee_id}")
def get_employee_documents(employee_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if current_user.role == "staff" and current_user.employee_id != employee_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if current_user.role == "project_manager" and not check_employee_access(current_user, employee_id, db):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    missing_docs = []
    doc_fields = {
        "Application/Resume": employee.missing_app_resume,
        "Appointment Letter": employee.missing_appointment_letter,
        "Academic Docs": employee.missing_academic_docs,
        "Staff ID Form": employee.missing_staff_id_form,
        "Performance Appraisals": employee.missing_performance_appraisals,
        "National ID": employee.missing_national_id,
        "Policy Declaration": employee.missing_policy_declaration,
        "End of Contract Notice": employee.missing_end_of_contract_notice,
    }
    
    for doc_name, is_missing in doc_fields.items():
        if is_missing:
            missing_docs.append(doc_name)
    
    return {"employee_id": employee_id, "full_name": employee.full_name, "missing_documents": missing_docs}
