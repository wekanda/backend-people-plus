from datetime import date, datetime, timezone
from typing import Literal, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
import models


router = APIRouter(prefix="/assets", tags=["assets"])
MANAGER_ROLES = {"hr_admin", "project_manager", "finance", "it_officer", "ceo", "ceo_assistant"}


class AssetCreate(BaseModel):
    tag_number: Optional[str] = None
    acquisition_date: Optional[date] = None
    name: str = Field(min_length=1, max_length=180)
    description: Optional[str] = None
    serial_number: str = Field(min_length=1, max_length=120)
    accessories: Optional[str] = None
    acquisition_type: str = "Purchase"
    department: str = Field(min_length=1, max_length=120)
    custodian: Optional[str] = None
    received_by: Optional[str] = None
    location: Optional[str] = None
    condition: Literal["Good", "Fair", "Poor"] = "Good"
    utilization_status: Literal["In use", "Underused", "Idle", "Under maintenance"] = "In use"
    asset_status: Literal["Active", "Retired", "Missing"] = "Active"
    last_count_date: Optional[date] = None


class AssetUpdate(BaseModel):
    tag_number: Optional[str] = None
    acquisition_date: Optional[date] = None
    name: Optional[str] = None
    description: Optional[str] = None
    serial_number: Optional[str] = None
    accessories: Optional[str] = None
    acquisition_type: Optional[str] = None
    department: Optional[str] = None
    custodian: Optional[str] = None
    received_by: Optional[str] = None
    location: Optional[str] = None
    condition: Optional[Literal["Good", "Fair", "Poor"]] = None
    utilization_status: Optional[Literal["In use", "Underused", "Idle", "Under maintenance"]] = None
    asset_status: Optional[Literal["Active", "Retired", "Missing"]] = None
    last_count_date: Optional[date] = None


def _require_manager(user):
    if user.role not in MANAGER_ROLES:
        raise HTTPException(status_code=403, detail="Insufficient permissions for asset management")


def _audit(db, user, action, asset_id, details):
    db.add(models.AuditLog(
        user_id=user.id,
        action=action,
        object_type="asset",
        object_id=str(asset_id),
        details=details,
    ))


@router.get("")
def list_assets(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_manager(current_user)
    return db.query(models.AssetRecord).order_by(models.AssetRecord.updated_at.desc()).all()


@router.post("", status_code=201)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_manager(current_user)
    tag_number = payload.tag_number or f"AST-{uuid4().hex[:8].upper()}"
    if db.query(models.AssetRecord).filter_by(tag_number=tag_number).first():
        raise HTTPException(status_code=409, detail="Asset tag number already exists")
    if db.query(models.AssetRecord).filter_by(serial_number=payload.serial_number).first():
        raise HTTPException(status_code=409, detail="Serial number already exists")

    asset = models.AssetRecord(**payload.model_dump(exclude={"tag_number"}), tag_number=tag_number, created_by=current_user.id)
    db.add(asset)
    db.flush()
    _audit(db, current_user, "created", asset.id, f"Asset {tag_number} registered")
    db.commit()
    db.refresh(asset)
    return asset


@router.patch("/{asset_id}")
def update_asset(asset_id: int, payload: AssetUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_manager(current_user)
    asset = db.query(models.AssetRecord).filter_by(id=asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    changes = payload.model_dump(exclude_unset=True)
    if changes.get("tag_number") and db.query(models.AssetRecord).filter(
        models.AssetRecord.tag_number == changes["tag_number"], models.AssetRecord.id != asset_id
    ).first():
        raise HTTPException(status_code=409, detail="Asset tag number already exists")
    if changes.get("serial_number") and db.query(models.AssetRecord).filter(
        models.AssetRecord.serial_number == changes["serial_number"], models.AssetRecord.id != asset_id
    ).first():
        raise HTTPException(status_code=409, detail="Serial number already exists")
    for key, value in changes.items():
        setattr(asset, key, value)
    asset.updated_at = datetime.now(timezone.utc)
    _audit(db, current_user, "updated", asset.id, f"Updated fields: {', '.join(changes)}")
    db.commit()
    db.refresh(asset)
    return asset


@router.delete("/{asset_id}", status_code=204)
def delete_asset(asset_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_manager(current_user)
    asset = db.query(models.AssetRecord).filter_by(id=asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    _audit(db, current_user, "deleted", asset.id, f"Asset {asset.tag_number} deleted")
    db.delete(asset)
    db.commit()