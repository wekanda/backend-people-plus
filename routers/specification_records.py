import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
import models


router = APIRouter(prefix="/api/specification", tags=["specification records"])
CATALOG_PATH = Path(__file__).resolve().parents[1] / "specification" / "catalog.json"
with CATALOG_PATH.open("r", encoding="utf-8") as catalog_file:
    CATALOG = json.load(catalog_file)
FORMS = {form["key"]: form for form in CATALOG["forms"]}

MODULE_ROLES = {
    "people": {"hr_admin", "project_manager", "it_officer", "ceo", "ceo_assistant", "staff"},
    "procurement": {"hr_admin", "project_manager", "finance", "it_officer", "ceo", "ceo_assistant", "staff"},
    "finance": {"hr_admin", "project_manager", "finance", "pay", "it_officer", "ceo", "ceo_assistant"},
    "assets": {"hr_admin", "project_manager", "finance", "it_officer", "ceo", "ceo_assistant"},
    "shared": {"hr_admin", "project_manager", "finance", "pay", "it_officer", "ceo", "ceo_assistant"},
}
WRITE_ROLES = {"hr_admin", "project_manager", "finance", "pay", "it_officer", "ceo", "ceo_assistant"}
STAFF_SELF_SERVICE = ("staff dashboard", "staff profile", "expense claim", "leave", "attendance", "timesheet", "training request", "procurement request", "stores request")


class SpecificationRecordCreate(BaseModel):
    form_key: str = Field(min_length=1, max_length=180)
    reference: Optional[str] = Field(default=None, max_length=180)
    status: str = Field(default="Draft", max_length=80)
    employee_id: Optional[int] = None
    values: dict = Field(default_factory=dict)


class SpecificationRecordUpdate(BaseModel):
    reference: Optional[str] = Field(default=None, max_length=180)
    status: Optional[str] = Field(default=None, max_length=80)
    employee_id: Optional[int] = None
    values: Optional[dict] = None


def _form_for(form_key, user):
    form = FORMS.get(form_key)
    if not form:
        raise HTTPException(status_code=404, detail="Specification form not found")
    if user.role not in MODULE_ROLES.get(form["module"], set()):
        raise HTTPException(status_code=403, detail="Your role cannot access this specification module")
    if user.role == "staff" and not any(word in form["title"].lower() for word in STAFF_SELF_SERVICE):
        raise HTTPException(status_code=403, detail="Staff can only use self-service specification forms")
    return form


def _validate_values(form, values):
    allowed = {field["name"]: field for field in form["fields"]}
    unknown = sorted(set(values) - set(allowed))
    if unknown:
        raise HTTPException(status_code=422, detail={"message": "Unknown form fields", "fields": unknown})
    result = {}
    for name, value in values.items():
        field = allowed[name]
        if value is None or value == "":
            result[name] = None
            continue
        if field["type"] == "number":
            try:
                result[name] = float(value)
            except (TypeError, ValueError):
                raise HTTPException(status_code=422, detail=f"{field['label']} must be numeric")
        elif field["type"] == "boolean":
            if not isinstance(value, bool):
                raise HTTPException(status_code=422, detail=f"{field['label']} must be true or false")
            result[name] = value
        else:
            result[name] = str(value)
    return result


def _record_view(record):
    return {
        "id": record.id,
        "form_key": record.form_key,
        "form_title": record.form_title,
        "module": record.module,
        "reference": record.reference,
        "status": record.status,
        "employee_id": record.employee_id,
        "values": json.loads(record.values_json or "{}"),
        "created_by": record.created_by,
        "updated_by": record.updated_by,
        "created_at": record.created_at.isoformat() if record.created_at else None,
        "updated_at": record.updated_at.isoformat() if record.updated_at else None,
    }


def _write_history(db, user, record, action, previous, current):
    previous = previous or {}
    current = current or {}
    previous_values = previous.get("values", previous)
    current_values = current.get("values", current)
    changed = [
        f"field:{key}" for key in sorted(set(previous_values) | set(current_values))
        if previous_values.get(key) != current_values.get(key)
    ]
    changed.extend(
        key for key in ("reference", "status", "employee_id")
        if previous.get(key) != current.get(key)
    )
    db.add(models.SpecificationRecordHistory(
        record_id=record.id,
        user_id=user.id,
        action=action,
        previous_values_json=json.dumps(previous, ensure_ascii=False),
        current_values_json=json.dumps(current, ensure_ascii=False),
        changed_fields_json=json.dumps(changed, ensure_ascii=False),
    ))
    db.add(models.AuditLog(
        user_id=user.id,
        action=action,
        object_type="specification_record",
        object_id=str(record.id),
        details=json.dumps({"form": record.form_key, "changed_fields": changed}, ensure_ascii=False),
    ))


@router.get("/catalog")
def get_catalog(module: Optional[str] = None, search: Optional[str] = None, user=Depends(get_current_user)):
    forms = [
        form for form in CATALOG["forms"]
        if user.role in MODULE_ROLES.get(form["module"], set())
        and (user.role != "staff" or any(word in form["title"].lower() for word in STAFF_SELF_SERVICE))
        and (not module or form["module"] == module)
        and (not search or search.lower() in form["title"].lower() or any(search.lower() in field["label"].lower() for field in form["fields"]))
    ]
    return {"form_count": len(forms), "field_count": sum(len(form["fields"]) for form in forms), "forms": forms}


@router.get("/forms/{form_key}")
def get_form(form_key: str, user=Depends(get_current_user)):
    return _form_for(form_key, user)


@router.get("/records")
def list_records(
    module: Optional[str] = None,
    form_key: Optional[str] = None,
    search: Optional[str] = None,
    include_deleted: bool = False,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    query = db.query(models.SpecificationRecord)
    if not include_deleted or user.role not in ("hr_admin", "it_officer"):
        query = query.filter(models.SpecificationRecord.is_deleted.is_(False))
    if module:
        if user.role not in MODULE_ROLES.get(module, set()):
            raise HTTPException(status_code=403, detail="Your role cannot access this module")
        query = query.filter_by(module=module)
    else:
        query = query.filter(models.SpecificationRecord.module.in_([
            key for key, roles in MODULE_ROLES.items() if user.role in roles
        ]))
    if form_key:
        _form_for(form_key, user)
        query = query.filter_by(form_key=form_key)
    if user.role == "staff":
        query = query.filter((models.SpecificationRecord.created_by == user.id) | (models.SpecificationRecord.employee_id == user.employee_id))
        self_service_forms = [
            form["key"] for form in CATALOG["forms"]
            if form["module"] == "people"
            and any(word in form["title"].lower() for word in STAFF_SELF_SERVICE)
        ]
        query = query.filter(models.SpecificationRecord.form_key.in_(self_service_forms))
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(
            models.SpecificationRecord.reference.ilike(pattern),
            models.SpecificationRecord.values_json.ilike(pattern),
            models.SpecificationRecord.form_title.ilike(pattern),
        ))
    total = query.count()
    rows = query.order_by(models.SpecificationRecord.updated_at.desc()).offset(skip).limit(limit).all()
    return {"total": total, "records": [_record_view(row) for row in rows]}


@router.post("/records", status_code=201)
def create_record(payload: SpecificationRecordCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    form = _form_for(payload.form_key, user)
    if user.role not in WRITE_ROLES and user.role != "staff":
        raise HTTPException(status_code=403, detail="Your role cannot create specification records")
    if user.role == "staff" and payload.employee_id not in (None, user.employee_id):
        raise HTTPException(status_code=403, detail="Staff can only create records for their own employee profile")
    values = _validate_values(form, payload.values)
    record = models.SpecificationRecord(
        form_key=form["key"],
        form_title=form["title"],
        module=form["module"],
        reference=payload.reference,
        status="Draft" if user.role == "staff" else payload.status,
        employee_id=payload.employee_id or user.employee_id if user.role == "staff" else payload.employee_id,
        values_json=json.dumps(values, ensure_ascii=False),
        created_by=user.id,
        updated_by=user.id,
    )
    db.add(record)
    db.flush()
    _write_history(db, user, record, "created", {}, {
        "values": values,
        "reference": record.reference,
        "status": record.status,
        "employee_id": record.employee_id,
    })
    db.commit()
    db.refresh(record)
    return _record_view(record)


@router.patch("/records/{record_id}")
def update_record(record_id: int, payload: SpecificationRecordUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = db.query(models.SpecificationRecord).filter_by(id=record_id, is_deleted=False).first()
    if not record:
        raise HTTPException(status_code=404, detail="Specification record not found")
    form = _form_for(record.form_key, user)
    if user.role not in WRITE_ROLES and not (user.role == "staff" and record.created_by == user.id):
        raise HTTPException(status_code=403, detail="Your role cannot update this record")
    if user.role == "staff" and (payload.status is not None or payload.employee_id is not None):
        raise HTTPException(status_code=403, detail="Staff cannot change record approval status or ownership")
    previous_values = json.loads(record.values_json or "{}")
    previous = {
        "values": previous_values,
        "reference": record.reference,
        "status": record.status,
        "employee_id": record.employee_id,
    }
    patch_values = _validate_values(form, payload.values) if payload.values is not None else {}
    values = {**previous_values, **patch_values}
    if payload.reference is not None:
        record.reference = payload.reference
    if payload.status is not None:
        record.status = payload.status
    if payload.employee_id is not None:
        record.employee_id = payload.employee_id
    record.values_json = json.dumps(values, ensure_ascii=False)
    record.updated_by = user.id
    record.updated_at = datetime.now(timezone.utc)
    _write_history(db, user, record, "updated", previous, {
        "values": values,
        "reference": record.reference,
        "status": record.status,
        "employee_id": record.employee_id,
    })
    db.commit()
    db.refresh(record)
    return _record_view(record)


@router.delete("/records/{record_id}", status_code=204)
def delete_record(record_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = db.query(models.SpecificationRecord).filter_by(id=record_id, is_deleted=False).first()
    if not record:
        raise HTTPException(status_code=404, detail="Specification record not found")
    _form_for(record.form_key, user)
    if user.role not in WRITE_ROLES:
        raise HTTPException(status_code=403, detail="Your role cannot delete specification records")
    previous = {
        "values": json.loads(record.values_json or "{}"),
        "reference": record.reference,
        "status": record.status,
        "employee_id": record.employee_id,
    }
    record.is_deleted = True
    record.updated_by = user.id
    record.updated_at = datetime.now(timezone.utc)
    _write_history(db, user, record, "deleted", previous, {})
    db.commit()


@router.get("/records/{record_id}/history")
def record_history(record_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = db.query(models.SpecificationRecord).filter_by(id=record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Specification record not found")
    _form_for(record.form_key, user)
    if user.role == "staff" and record.created_by != user.id and record.employee_id != user.employee_id:
        raise HTTPException(status_code=403, detail="Cannot view another user's record history")
    entries = db.query(models.SpecificationRecordHistory).filter_by(record_id=record_id).order_by(models.SpecificationRecordHistory.created_at.asc()).all()
    return [{
        "id": entry.id,
        "user_id": entry.user_id,
        "action": entry.action,
        "previous_values": json.loads(entry.previous_values_json or "{}"),
        "current_values": json.loads(entry.current_values_json or "{}"),
        "changed_fields": json.loads(entry.changed_fields_json or "[]"),
        "created_at": entry.created_at.isoformat() if entry.created_at else None,
    } for entry in entries]