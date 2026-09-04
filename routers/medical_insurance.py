"""
Medical Insurance - populate beneficiaries, generate cover records, submit and
approve. Workflow: draft -> generated -> submitted -> approved.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from database import get_db
import models
from auth import get_current_user

router = APIRouter(prefix="/api/medical-insurance", tags=["medical-insurance"])


def _detail(ben: models.MedicalInsuranceBeneficiary, db: Session) -> dict:
    employee = db.query(models.Employee).filter(models.Employee.id == ben.employee_id).first()
    return {
        "id": ben.id,
        "employee_id": ben.employee_id,
        "employee_name": employee.full_name if employee else None,
        "file_code": employee.file_code if employee else None,
        "full_name": ben.full_name,
        "relationship": ben.relationship or "Self",
        "date_of_birth": str(ben.date_of_birth) if ben.date_of_birth else None,
        "national_id": ben.national_id,
        "passport_photo_url": ben.passport_photo_url,
        "cover_type": ben.cover_type or "Inpatient & Outpatient",
        "policy_number": ben.policy_number,
        "status": ben.status,
        "generated_at": str(ben.generated_at) if ben.generated_at else None,
        "submitted_at": str(ben.submitted_at) if ben.submitted_at else None,
        "approved_at": str(ben.approved_at) if ben.approved_at else None,
    }


@router.get("/beneficiaries")
def list_beneficiaries(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """List all medical insurance beneficiaries (HR / Finance / Pay)."""
    if current_user.role not in ("hr_admin", "project_manager", "finance", "pay"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    items = db.query(models.MedicalInsuranceBeneficiary).order_by(models.MedicalInsuranceBeneficiary.id.desc()).all()
    return [_detail(b, db) for b in items]


@router.get("/state")
def insurance_state(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Workflow state summary: drafts, generated, submitted, approved."""
    if current_user.role not in ("hr_admin", "project_manager", "finance", "pay"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    rows = db.query(models.MedicalInsuranceBeneficiary.status).all()
    counts = {"draft": 0, "generated": 0, "submitted": 0, "approved": 0}
    for (s,) in rows:
        counts[s] = counts.get(s, 0) + 1
    return {"total": len(rows), "counts": counts, "workflow": ["draft", "generated", "submitted", "approved"]}


@router.post("/beneficiaries")
def populate_beneficiary(payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Populate a medical insurance beneficiary from staff information."""
    if current_user.role not in ("hr_admin", "project_manager", "finance", "pay"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    employee_id = payload.get("employee_id")
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    ben = models.MedicalInsuranceBeneficiary(
        employee_id=employee_id,
        full_name=payload.get("full_name") or employee.full_name,
        relationship=payload.get("relationship") or "Self",
        date_of_birth=payload.get("date_of_birth") or employee.date_of_birth,
        national_id=payload.get("national_id"),
        passport_photo_url=payload.get("passport_photo_url") or employee.passport_photo_url,
        cover_type=payload.get("cover_type") or "Inpatient & Outpatient",
        policy_number=payload.get("policy_number"),
        created_by=current_user.id,
    )
    db.add(ben)
    db.commit()
    db.refresh(ben)
    return _detail(ben, db)
@router.post("/beneficiaries/{ben_id}/generate")
def generate_beneficiary(ben_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Generate the medical insurance record (draft -> generated)."""
    if current_user.role not in ("hr_admin", "project_manager", "finance", "pay"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    ben = db.query(models.MedicalInsuranceBeneficiary).filter(models.MedicalInsuranceBeneficiary.id == ben_id).first()
    if not ben:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    if ben.status == "approved":
        raise HTTPException(status_code=400, detail="Already approved, cannot re-generate")
    ben.status = "generated"
    ben.generated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(ben)
    return _detail(ben, db)


@router.post("/beneficiaries/{ben_id}/submit")
def submit_beneficiary(ben_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Submit generated medical insurance records for approval."""
    if current_user.role not in ("hr_admin", "project_manager", "finance", "pay"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    ben = db.query(models.MedicalInsuranceBeneficiary).filter(models.MedicalInsuranceBeneficiary.id == ben_id).first()
    if not ben:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    if ben.status not in ("generated", "draft"):
        raise HTTPException(status_code=400, detail="Only generated/draft beneficiaries can be submitted")
    ben.status = "submitted"
    ben.submitted_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(ben)
    return _detail(ben, db)


@router.post("/beneficiaries/{ben_id}/approve")
def approve_beneficiary(ben_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Approve a submitted medical insurance beneficiary."""
    if current_user.role not in ("hr_admin", "finance"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    ben = db.query(models.MedicalInsuranceBeneficiary).filter(models.MedicalInsuranceBeneficiary.id == ben_id).first()
    if not ben:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    if ben.status != "submitted":
        raise HTTPException(status_code=400, detail="Only submitted beneficiaries can be approved")
    ben.status = "approved"
    ben.approved_by = current_user.id
    ben.approved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(ben)
    return _detail(ben, db)


@router.post("/beneficiaries/{ben_id}/reset")
def reset_beneficiary(ben_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Reset a beneficiary to draft for rework."""
    if current_user.role not in ("hr_admin", "project_manager", "finance", "pay"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    ben = db.query(models.MedicalInsuranceBeneficiary).filter(models.MedicalInsuranceBeneficiary.id == ben_id).first()
    if not ben:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    if ben.status == "approved":
        raise HTTPException(status_code=400, detail="Approved records cannot be reset")
    ben.status = "draft"
    ben.generated_at = None
    ben.submitted_at = None
    db.commit()
    db.refresh(ben)
    return _detail(ben, db)


@router.delete("/beneficiaries/{ben_id}")
def delete_beneficiary(ben_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Delete a draft beneficiary record."""
    if current_user.role not in ("hr_admin", "project_manager"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    ben = db.query(models.MedicalInsuranceBeneficiary).filter(models.MedicalInsuranceBeneficiary.id == ben_id).first()
    if not ben:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    db.delete(ben)
    db.commit()
    return {"ok": True, "message": "Beneficiary removed"}