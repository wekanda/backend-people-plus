"""
Signatures & Electronic Stamps - digital signature uploads for all roles, the
official HR electronic stamp, and passport / full-length photo uploads that feed
ID generation, medical insurance, birthdays and employee recognition.
"""
from datetime import datetime, timezone
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


@router.get("/signatures/employee/{employee_id}")
def list_employee_signatures(employee_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Return all signature records for an employee. Only the employee or an authorized manager may view them."""
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if not check_employee_access(current_user, employee_id, db):
        raise HTTPException(status_code=403, detail="Access denied")

    signatures = (
        db.query(models.EmployeeSignature)
        .filter(models.EmployeeSignature.employee_id == employee_id)
        .order_by(models.EmployeeSignature.uploaded_at.desc())
        .all()
    )
    return {
        "employee_id": employee_id,
        "items": [
            {
                "id": s.id,
                "employee_id": s.employee_id,
                "uploaded_by": s.uploaded_by,
                "signature_type": s.signature_type,
                "file_name": s.file_name,
                "file_path": s.file_path,
                "signature_url": s.file_path,
                "uploaded_at": s.uploaded_at.isoformat() if s.uploaded_at else None,
                "status": s.status,
                "verified_by": s.verified_by,
                "verified_at": s.verified_at.isoformat() if s.verified_at else None,
                "rejection_reason": s.rejection_reason,
                "replaces_signature_id": s.replaces_signature_id,
                "replaced_by_id": s.replaced_by_id,
                "archived_at": s.archived_at.isoformat() if s.archived_at else None,
            }
            for s in signatures
        ],
    }


@router.post("/signatures/employee/{employee_id}")
async def upload_employee_signature(
    employee_id: int,
    file: UploadFile = File(...),
    signature_type: str = "primary",
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Upload a verified employee signature image; stores the file and records the lifecycle for the personnel file."""
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if not check_employee_access(current_user, employee_id, db):
        raise HTTPException(status_code=403, detail="Access denied")
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    allowed_types = {"primary", "initials", "acknowledgement"}
    normalized_type = (signature_type or "primary").strip().lower()
    if normalized_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid signature_type. Use primary, initials, or acknowledgement.")

    relative_url = _save_upload("employee_signatures", employee_id, file)
    record = models.EmployeeSignature(
        employee_id=employee_id,
        uploaded_by=current_user.id,
        signature_type=normalized_type,
        file_path=relative_url,
        file_name=file.filename,
        status="Pending Verification",
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    audit = models.SignatureAudit(
        signature_id=record.id,
        employee_id=employee_id,
        actor_id=current_user.id,
        action="uploaded",
        document_type="employee_signature",
        details=f"{current_user.full_name or current_user.email} uploaded a {normalized_type} signature",
    )
    db.add(audit)
    db.commit()

    return {
        "id": record.id,
        "employee_id": record.employee_id,
        "uploaded_by": record.uploaded_by,
        "signature_type": record.signature_type,
        "file_name": record.file_name,
        "file_path": record.file_path,
        "signature_url": record.file_path,
        "uploaded_at": record.uploaded_at.isoformat() if record.uploaded_at else None,
        "status": record.status,
    }


@router.post("/signatures/employee/{employee_id}/verify")
def verify_employee_signature(
    employee_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Verify or reject a previously uploaded employee signature."""
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if current_user.role not in ("hr_admin", "it_officer", "project_manager", "ceo", "ceo_assistant"):
        raise HTTPException(status_code=403, detail="Only authorized HR or management roles can verify signatures")

    signature_id = payload.get("signature_id")
    status = (payload.get("status") or "").strip()
    if not signature_id:
        raise HTTPException(status_code=400, detail="signature_id is required")
    if status not in ("verified", "rejected", "Pending Verification"):
        raise HTTPException(status_code=400, detail="status must be verified, rejected, or Pending Verification")

    signature = db.query(models.EmployeeSignature).filter(models.EmployeeSignature.id == signature_id).first()
    if not signature or signature.employee_id != employee_id:
        raise HTTPException(status_code=404, detail="Signature not found for this employee")

    signature.status = status
    signature.verified_by = current_user.id
    signature.verified_at = datetime.now(timezone.utc)
    signature.rejection_reason = payload.get("rejection_reason") if status == "rejected" else None
    db.add(signature)
    db.commit()
    db.refresh(signature)

    audit = models.SignatureAudit(
        signature_id=signature.id,
        employee_id=employee_id,
        actor_id=current_user.id,
        action=status,
        document_type="employee_signature",
        details=payload.get("rejection_reason") if status == "rejected" else "Employee signature verified",
    )
    db.add(audit)
    db.commit()

    return {
        "id": signature.id,
        "employee_id": signature.employee_id,
        "status": signature.status,
        "verified_by": signature.verified_by,
        "verified_at": signature.verified_at.isoformat() if signature.verified_at else None,
        "rejection_reason": signature.rejection_reason,
    }


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
    if current_user.role not in ("hr_admin", "it_officer"):
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