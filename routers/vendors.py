"""Vendor / supplier master data endpoints.

Datapoints from the People Pulse Unified Master Specification:
Vendor ID, Vendor Name, TIN, Registration Number, Bank Information,
Contact Information, Compliance Documents, Performance Rating.
"""
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
import models

router = APIRouter(prefix="/api/vendors", tags=["vendors"])

MANAGER_ROLES = {"hr_admin", "project_manager", "finance", "it_officer", "ceo", "ceo_assistant"}
FINANCE_ROLES = {"hr_admin", "finance", "it_officer", "ceo", "ceo_assistant"}


def _require(user, roles):
    if user.role not in roles:
        raise HTTPException(status_code=403, detail="Insufficient permissions")


def _audit(db, user, action, vendor_id, details):
    db.add(models.AuditLog(
        user_id=user.id,
        action=action,
        object_type="vendor",
        object_id=str(vendor_id),
        details=details,
    ))


class VendorCreate(BaseModel):
    vendor_code: Optional[str] = None
    vendor_name: str = Field(min_length=1, max_length=200)
    category: Optional[str] = None
    tin: Optional[str] = None
    registration_number: Optional[str] = None
    bank_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_branch: Optional[str] = None
    sort_code: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = "Uganda"
    compliance_documents: Optional[str] = None   # JSON list
    performance_rating: Optional[float] = None   # 0-5
    status: str = "Active"
    notes: Optional[str] = None


class VendorUpdate(BaseModel):
    vendor_name: Optional[str] = None
    category: Optional[str] = None
    tin: Optional[str] = None
    registration_number: Optional[str] = None
    bank_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_branch: Optional[str] = None
    sort_code: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    compliance_documents: Optional[str] = None
    performance_rating: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None


@router.get("")
def list_vendors(status: Optional[str] = None, search: Optional[str] = None,
                 db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require(current_user, MANAGER_ROLES)
    query = db.query(models.Vendor)
    if status:
        query = query.filter(models.Vendor.status == status)
    if search:
        term = f"%{search}%"
        query = query.filter(
            (models.Vendor.vendor_name.ilike(term)) |
            (models.Vendor.vendor_code.ilike(term)) |
            (models.Vendor.tin.ilike(term))
        )
    return query.order_by(models.Vendor.vendor_name.asc()).all()


@router.post("", status_code=201)
def create_vendor(payload: VendorCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require(current_user, FINANCE_ROLES)
    vendor_code = payload.vendor_code or (payload.vendor_name[:3].upper() + "-" + uuid4().hex[:6].upper())
    if db.query(models.Vendor).filter_by(vendor_code=vendor_code).first():
        raise HTTPException(status_code=409, detail="Vendor code already exists")
    if payload.tin and db.query(models.Vendor).filter_by(tin=payload.tin).first():
        raise HTTPException(status_code=409, detail="A vendor with this TIN already exists")

    vendor = models.Vendor(**payload.model_dump(exclude={"vendor_code"}), vendor_code=vendor_code, created_by=current_user.id)
    db.add(vendor)
    db.flush()
    _audit(db, current_user, "created", vendor.id, f"Vendor {vendor_code} created")
    db.commit()
    db.refresh(vendor)
    return vendor


@router.patch("/{vendor_id}")
def update_vendor(vendor_id: int, payload: VendorUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require(current_user, FINANCE_ROLES)
    vendor = db.query(models.Vendor).filter_by(id=vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    changes = payload.model_dump(exclude_unset=True)
    if changes.get("tin") and db.query(models.Vendor).filter(
        models.Vendor.tin == changes["tin"], models.Vendor.id != vendor_id
    ).first():
        raise HTTPException(status_code=409, detail="A vendor with this TIN already exists")
    for key, value in changes.items():
        setattr(vendor, key, value)
    vendor.updated_at = datetime.now(timezone.utc)
    _audit(db, current_user, "updated", vendor.id, f"Updated fields: {', '.join(changes)}")
    db.commit()
    db.refresh(vendor)
    return vendor


@router.delete("/{vendor_id}", status_code=204)
def delete_vendor(vendor_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require(current_user, FINANCE_ROLES)
    vendor = db.query(models.Vendor).filter_by(id=vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    _audit(db, current_user, "deleted", vendor.id, f"Vendor {vendor.vendor_name} deleted")
    db.delete(vendor)
    db.commit()
