"""
Signatures & Electronic Stamps - digital signature uploads for all roles, the
official HR electronic stamp, and passport / full-length photo uploads that feed
ID generation, medical insurance, birthdays and employee recognition.
"""
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db
import models
from auth import get_current_user, check_employee_access

router = APIRouter(prefix="/api", tags=["signatures & stamps"])

UPLOAD_ROOT = Path("uploads")


def _save_upload(subfolder: str, employee_id: int, file: UploadFile):
    folder = UPLOAD_ROOT / subfolder
    folder.mkdir(parents=True, exist_ok=True)
    suffix = Path(file.filename or "file.png").suffix.lower() or ".png"
    filename = f"{employee_id}_{uuid4().hex}{suffix}"
    destination = folder / filename
    contents = file.file.read()
    destination.write_bytes(contents)
    return f"/uploads/{subfolder}/{filename}"


@router.get("/signatures/me")
def get_my_signature(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Return the current user's uploaded digital signature (if any)."""
    signature = (
        db.query(models.UserSignature)
        .filter(models.UserSignature.user_id == current_user.id)
        .order_by(models.UserSignature.id.desc())
        .first()
    )
    return {"has_signature": bool(signature), "signature_url": getattr(signature, "signature_url", None)}


@router.post("/signatures")
async def upload_signature(file: UploadFile = File(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Upload a personal digital signature (sign on white paper, scan/photo, upload).

    Available to all authenticated roles: hr_admin, project_manager, staff, finance.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    url = _save_upload("signatures", current_user.id, file)
    record = models.UserSignature(user_id=current_user.id, signature_url=url)
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"ok": True, "signature_url": url}


@router.get("/hr-stamp")
def get_hr_stamp(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Return the official HR electronic stamp used to authenticate documents."""
    stamp = db.query(models.HRStamp).order_by(models.HRStamp.id.desc()).first()
    if not stamp:
        return {"has_stamp": False, "stamp_url": None, "label": "HR Official Stamp"}
    return {"has_stamp": True, "stamp_url": stamp.stamp_url, "label": stamp.label}


@router.post("/hr-stamp")
async def upload_hr_stamp(file: UploadFile = File(...), label: str = "HR Official Stamp", db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Upload the official electronic HR / People & Culture stamp (HR admin only)."""
    if current_user.role != "hr_admin":
        raise HTTPException(status_code=403, detail="Only HR Admin may upload the official stamp")
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    url = _save_upload("hr_stamp", current_user.id, file)
    record = models.HRStamp(stamp_url=url, label=label, uploaded_by=current_user.id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"ok": True, "stamp_url": url, "label": record.label}


@router.post("/employees/{employee_id}/photos/{photo_kind}")
async def upload_employee_photo_kind(
    employee_id: int,
    photo_kind: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Upload a passport photo (photo_kind=passport) or full-length photo
    (photo_kind=full) for an employee. Changes are saved to
    employee.passport_photo_url / employee.full_photo_url."""
    if photo_kind not in ("passport", "full"):
        raise HTTPException(status_code=400, detail="photo_kind must be 'passport' or 'full'")
    if not check_employee_access(current_user, employee_id, db):
        raise HTTPException(status_code=403, detail="Access denied")

    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    url = _save_upload("employee_photos", employee_id, file)
    if photo_kind == "passport":
        employee.passport_photo_url = url
    else:
        employee.full_photo_url = url
    db.commit()
    db.refresh(employee)
    return {
        "ok": True,
        "photo_kind": photo_kind,
        "photo_url": url,
        "passport_photo_url": employee.passport_photo_url,
        "full_photo_url": employee.full_photo_url,
    }