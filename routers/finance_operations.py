from datetime import date, datetime, timezone
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
import models


router = APIRouter(prefix="/finance", tags=["finance operations"])
READ_ROLES = {"hr_admin", "project_manager", "finance", "pay", "it_officer", "ceo", "ceo_assistant"}
WRITE_ROLES = {"hr_admin", "finance", "pay", "it_officer"}


class FinanceEntryCreate(BaseModel):
    category: Literal["budget", "cash", "report", "control", "risk", "audit"]
    title: str = Field(min_length=1, max_length=180)
    description: Optional[str] = None
    department: Optional[str] = None
    period: Optional[str] = None
    direction: Optional[Literal["inflow", "outflow"]] = None
    amount: float = Field(default=0, ge=0)
    committed_amount: float = Field(default=0, ge=0)
    actual_amount: float = Field(default=0, ge=0)
    status: str = "Open"
    due_date: Optional[date] = None
    owner: Optional[str] = None
    evidence_reference: Optional[str] = None


class FinanceEntryUpdate(BaseModel):
    category: Optional[Literal["budget", "cash", "report", "control", "risk", "audit"]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    department: Optional[str] = None
    period: Optional[str] = None
    direction: Optional[Literal["inflow", "outflow"]] = None
    amount: Optional[float] = Field(default=None, ge=0)
    committed_amount: Optional[float] = Field(default=None, ge=0)
    actual_amount: Optional[float] = Field(default=None, ge=0)
    status: Optional[str] = None
    due_date: Optional[date] = None
    owner: Optional[str] = None
    evidence_reference: Optional[str] = None


class PAYECreate(BaseModel):
    period: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    due_date: Optional[date] = None
    paye_amount: float = Field(default=0, ge=0)
    salary_deductions_processed: bool = False
    monthly_return_filed: bool = False
    return_filed_date: Optional[date] = None
    remitted: bool = False
    remittance_date: Optional[date] = None
    penalty_amount: float = Field(default=0, ge=0)
    interest_amount: float = Field(default=0, ge=0)
    audit_status: str = "Not scheduled"
    notes: Optional[str] = None


class PAYEUpdate(BaseModel):
    due_date: Optional[date] = None
    paye_amount: Optional[float] = Field(default=None, ge=0)
    salary_deductions_processed: Optional[bool] = None
    monthly_return_filed: Optional[bool] = None
    return_filed_date: Optional[date] = None
    remitted: Optional[bool] = None
    remittance_date: Optional[date] = None
    penalty_amount: Optional[float] = Field(default=None, ge=0)
    interest_amount: Optional[float] = Field(default=None, ge=0)
    audit_status: Optional[str] = None
    notes: Optional[str] = None


def _require_access(user, write=False):
    allowed = WRITE_ROLES if write else READ_ROLES
    if user.role not in allowed:
        raise HTTPException(status_code=403, detail="Insufficient permissions for finance records")


def _audit(db, user, action, object_type, object_id, details):
    db.add(models.AuditLog(
        user_id=user.id,
        action=action,
        object_type=object_type,
        object_id=str(object_id),
        details=details,
    ))


@router.get("/operations")
def list_finance_entries(category: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_access(current_user)
    query = db.query(models.FinanceRegisterEntry)
    if category:
        query = query.filter_by(category=category)
    return query.order_by(models.FinanceRegisterEntry.updated_at.desc()).all()


@router.post("/operations", status_code=201)
def create_finance_entry(payload: FinanceEntryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_access(current_user, write=True)
    entry = models.FinanceRegisterEntry(**payload.model_dump(), created_by=current_user.id)
    db.add(entry)
    db.flush()
    _audit(db, current_user, "created", "finance_entry", entry.id, f"{entry.category}: {entry.title}")
    db.commit()
    db.refresh(entry)
    return entry


@router.patch("/operations/{entry_id}")
def update_finance_entry(entry_id: int, payload: FinanceEntryUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_access(current_user, write=True)
    entry = db.query(models.FinanceRegisterEntry).filter_by(id=entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Finance entry not found")
    changes = payload.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(entry, key, value)
    entry.updated_at = datetime.now(timezone.utc)
    _audit(db, current_user, "updated", "finance_entry", entry.id, f"Updated fields: {', '.join(changes)}")
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/operations/{entry_id}", status_code=204)
def delete_finance_entry(entry_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_access(current_user, write=True)
    entry = db.query(models.FinanceRegisterEntry).filter_by(id=entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Finance entry not found")
    _audit(db, current_user, "deleted", "finance_entry", entry.id, f"{entry.category}: {entry.title}")
    db.delete(entry)
    db.commit()


@router.get("/paye-compliance")
def list_paye_records(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_access(current_user)
    return db.query(models.PAYEComplianceRecord).order_by(models.PAYEComplianceRecord.period.desc()).all()


@router.post("/paye-compliance", status_code=201)
def create_paye_record(payload: PAYECreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_access(current_user, write=True)
    if db.query(models.PAYEComplianceRecord).filter_by(period=payload.period).first():
        raise HTTPException(status_code=409, detail="A PAYE record already exists for this period")
    record = models.PAYEComplianceRecord(**payload.model_dump(), created_by=current_user.id)
    db.add(record)
    db.flush()
    _audit(db, current_user, "created", "paye_compliance", record.id, f"PAYE compliance for {record.period}")
    db.commit()
    db.refresh(record)
    return record


@router.patch("/paye-compliance/{record_id}")
def update_paye_record(record_id: int, payload: PAYEUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_access(current_user, write=True)
    record = db.query(models.PAYEComplianceRecord).filter_by(id=record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="PAYE compliance record not found")
    changes = payload.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(record, key, value)
    record.updated_at = datetime.now(timezone.utc)
    _audit(db, current_user, "updated", "paye_compliance", record.id, f"Updated fields: {', '.join(changes)}")
    db.commit()
    db.refresh(record)
    return record


@router.delete("/paye-compliance/{record_id}", status_code=204)
def delete_paye_record(record_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_access(current_user, write=True)
    record = db.query(models.PAYEComplianceRecord).filter_by(id=record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="PAYE compliance record not found")
    _audit(db, current_user, "deleted", "paye_compliance", record.id, f"PAYE compliance for {record.period}")
    db.delete(record)
    db.commit()