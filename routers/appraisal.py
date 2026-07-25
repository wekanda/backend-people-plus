from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from pydantic import BaseModel
import models
from database import get_db
from auth import get_current_user, check_employee_access
from typing import List

router = APIRouter(prefix="/api/appraisal", tags=["appraisal"])

class AppraisalCreate(BaseModel):
    employee_id: int
    position: str
    duration_in_position: str
    achievements: str
    challenges: str
    point_outs: str = None

class AppraisalResponse(BaseModel):
    id: int
    employee_id: int
    position: str
    duration_in_position: str | None = None
    achievements: str
    challenges: str
    point_outs: str | None = None
    appraisal_date: date
    class Config:
        from_attributes = True

@router.post("/create", response_model=AppraisalResponse)
def create_appraisal(appraisal: AppraisalCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role not in ("hr_admin", "project_manager"):
        raise HTTPException(status_code=403, detail="Insufficient permissions to create appraisals")

    db_appraisal = models.PerformanceAppraisal(
        **appraisal.dict(),
        appraisal_date=date.today(),
        reviewer_id=current_user.id
    )
    db.add(db_appraisal)
    db.commit()
    db.refresh(db_appraisal)
    return db_appraisal

@router.get("/employee/{employee_id}", response_model=List[AppraisalResponse])
def get_employee_appraisals(employee_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not check_employee_access(current_user, employee_id, db):
        raise HTTPException(status_code=403, detail="Insufficient permissions to view these appraisals")
    return db.query(models.PerformanceAppraisal).filter(models.PerformanceAppraisal.employee_id == employee_id).all()

@router.get("/", response_model=List[AppraisalResponse])
def list_appraisals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role not in ("hr_admin", "project_manager"):
        raise HTTPException(status_code=403, detail="Insufficient permissions to list appraisals")
    return db.query(models.PerformanceAppraisal).order_by(models.PerformanceAppraisal.appraisal_date.desc()).offset(skip).limit(limit).all()

@router.get("/{appraisal_id}", response_model=AppraisalResponse)
def get_appraisal(appraisal_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    appraisal = db.query(models.PerformanceAppraisal).filter(models.PerformanceAppraisal.id == appraisal_id).first()
    if not appraisal:
        raise HTTPException(status_code=404, detail="Appraisal not found")
    if current_user.role == "staff" and appraisal.employee_id != current_user.employee_id:
        raise HTTPException(status_code=403, detail="Insufficient permissions to view this appraisal")
    if current_user.role == "project_manager" and not check_employee_access(current_user, appraisal.employee_id, db):
        raise HTTPException(status_code=403, detail="Insufficient permissions to view this appraisal")
    return appraisal
