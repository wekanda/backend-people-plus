"""Organization & Department master data endpoints.

Datapoints from the People Pulse Unified Master Specification:
Organization, Branch, Region, Department, Unit, Project, Cost Center,
Budget Line, Funding Source.
"""
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
import models

router = APIRouter(prefix="/api/organization", tags=["organization"])

MANAGER_ROLES = {"hr_admin", "project_manager", "finance", "it_officer", "ceo", "ceo_assistant"}


def _require(user):
    if user.role not in MANAGER_ROLES:
        raise HTTPException(status_code=403, detail="Insufficient permissions")


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    org_type: Optional[str] = None
    registration_number: Optional[str] = None
    tin: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    currency: Optional[str] = None
    financial_year_start: Optional[str] = None
    branches_json: Optional[str] = None


@router.get("")
def get_organization(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require(current_user)
    org = db.query(models.Organization).first()
    if not org:
        return {}
    return org


@router.post("")
def create_organization(payload: OrganizationUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require(current_user)
    existing = db.query(models.Organization).first()
    if existing:
        for key, value in payload.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(existing, key, value)
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(existing)
        return existing
    org = models.Organization(**payload.model_dump(exclude_unset=True), created_by=current_user.id)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


class DepartmentCreate(BaseModel):
    name: str
    code: Optional[str] = None
    branch: Optional[str] = None
    region: Optional[str] = None
    organization_id: Optional[int] = None
    manager_id: Optional[int] = None
    cost_center: Optional[str] = None
    budget_line: Optional[str] = None
    parent_department: Optional[str] = None
    description: Optional[str] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    branch: Optional[str] = None
    region: Optional[str] = None
    organization_id: Optional[int] = None
    manager_id: Optional[int] = None
    cost_center: Optional[str] = None
    budget_line: Optional[str] = None
    parent_department: Optional[str] = None
    description: Optional[str] = None


@router.get("/departments")
def list_departments(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require(current_user)
    return db.query(models.Department).order_by(models.Department.name.asc()).all()


@router.post("/departments", status_code=201)
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require(current_user)
    dept = models.Department(**payload.model_dump(), created_by=current_user.id)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


@router.patch("/departments/{department_id}")
def update_department(department_id: int, payload: DepartmentUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require(current_user)
    dept = db.query(models.Department).filter_by(id=department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(dept, key, value)
    db.commit()
    db.refresh(dept)
    return dept


@router.delete("/departments/{department_id}", status_code=204)
def delete_department(department_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _require(current_user)
    dept = db.query(models.Department).filter_by(id=department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(dept)
    db.commit()
