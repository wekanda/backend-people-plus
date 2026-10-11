from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
import models


router = APIRouter(prefix="/procurement", tags=["procurement"])

STAGES = (
    "purchase_request",
    "request_for_quotation",
    "quotation_analysis",
    "award",
    "local_purchase_order",
    "delivery_note",
    "attendance_lists",
    "distribution_lists",
    "acknowledgement_forms",
    "invoicing",
)
MANAGER_ROLES = {"hr_admin", "project_manager", "finance", "it_officer", "ceo", "ceo_assistant"}


class ProcurementRequestCreate(BaseModel):
    request_number: Optional[str] = Field(default=None, max_length=64)
    department: str = Field(min_length=1, max_length=120)
    item_description: str = Field(min_length=1)
    quantity: int = Field(default=1, gt=0)
    estimated_amount: float = Field(default=0, ge=0)
    supplier: Optional[str] = None
    awarded_amount: float = Field(default=0, ge=0)
    date_requested: Optional[datetime] = None
    notes: Optional[str] = None


class ProcurementStageUpdate(BaseModel):
    stage: Literal[
        "request_for_quotation", "quotation_analysis", "award",
        "local_purchase_order", "delivery_note", "attendance_lists",
        "distribution_lists", "acknowledgement_forms", "invoicing",
    ]
    reference: Optional[str] = None
    notes: Optional[str] = None
    supplier: Optional[str] = None
    awarded_amount: Optional[float] = Field(default=None, ge=0)


def _require_manager(user):
    if user.role not in MANAGER_ROLES:
        raise HTTPException(status_code=403, detail="Insufficient permissions for procurement")


def _log_event(db, user, action, request_id, details):
    db.add(models.AuditLog(
        user_id=user.id,
        action=action,
        object_type="procurement_request",
        object_id=str(request_id),
        details=details,
    ))


@router.get("")
def list_requests(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_manager(current_user)
    requests = db.query(models.ProcurementRequest).order_by(models.ProcurementRequest.updated_at.desc()).all()
    result = []
    for request in requests:
        record = {column.name: getattr(request, column.name) for column in request.__table__.columns}
        record["history"] = db.query(models.ProcurementStageEvent).filter(
            models.ProcurementStageEvent.request_id == request.id
        ).order_by(models.ProcurementStageEvent.created_at.asc()).all()
        result.append(record)
    return result


@router.post("", status_code=201)
def create_request(payload: ProcurementRequestCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_manager(current_user)
    request_number = payload.request_number or f"PR-{uuid4().hex[:8].upper()}"
    if db.query(models.ProcurementRequest).filter_by(request_number=request_number).first():
        raise HTTPException(status_code=409, detail="Request number already exists")

    request = models.ProcurementRequest(
        request_number=request_number,
        department=payload.department.strip(),
        item_description=payload.item_description.strip(),
        quantity=payload.quantity,
        estimated_amount=payload.estimated_amount,
        supplier=payload.supplier,
        awarded_amount=payload.awarded_amount,
        date_requested=payload.date_requested.date() if payload.date_requested else None,
        notes=payload.notes,
        requested_by=current_user.id,
    )
    db.add(request)
    db.flush()
    db.add(models.ProcurementStageEvent(
        request_id=request.id,
        to_stage="purchase_request",
        notes="Purchase request created",
        changed_by=current_user.id,
    ))
    _log_event(db, current_user, "created", request.id, "Purchase request created")
    db.commit()
    db.refresh(request)
    return request


@router.patch("/{request_id}/stage")
def advance_request(request_id: int, payload: ProcurementStageUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_manager(current_user)
    request = db.query(models.ProcurementRequest).filter_by(id=request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Procurement request not found")
    current_index = STAGES.index(request.stage)
    if current_index >= len(STAGES) - 1 or STAGES[current_index + 1] != payload.stage:
        raise HTTPException(status_code=400, detail="Procurement stages must be completed in order")

    previous_stage = request.stage
    request.stage = payload.stage
    if payload.supplier:
        request.supplier = payload.supplier
    if payload.awarded_amount is not None:
        request.awarded_amount = payload.awarded_amount
    request.updated_at = datetime.now(timezone.utc)
    db.add(models.ProcurementStageEvent(
        request_id=request.id,
        from_stage=previous_stage,
        to_stage=payload.stage,
        reference=payload.reference,
        notes=payload.notes,
        changed_by=current_user.id,
    ))
    _log_event(db, current_user, "stage_advanced", request.id, f"{previous_stage} -> {payload.stage}; reference={payload.reference or ''}")
    db.commit()
    db.refresh(request)
    return request


@router.delete("/{request_id}", status_code=204)
def delete_request(request_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require_manager(current_user)
    request = db.query(models.ProcurementRequest).filter_by(id=request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Procurement request not found")
    _log_event(db, current_user, "deleted", request.id, f"Request {request.request_number} deleted")
    db.query(models.ProcurementStageEvent).filter_by(request_id=request.id).delete()
    db.delete(request)
    db.commit()