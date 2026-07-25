from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from pydantic import BaseModel
import models
from database import get_db
from auth import get_current_user
from typing import List
from sqlalchemy import func

def resolve_employee_id(current_user, db: Session):
    if current_user.employee_id is not None:
        return current_user.employee_id
    employee = db.query(models.Employee).filter(models.Employee.personal_email == current_user.email).first()
    return employee.id if employee else None
router = APIRouter(prefix="/api/timesheet", tags=["timesheet"])

class TimesheetCreate(BaseModel):
    employee_id: int
    date: date
    hours_worked: float
    overtime_hours: float = 0

class TimesheetResponse(BaseModel):
    id: int
    employee_id: int
    date: date
    hours_worked: float
    overtime_hours: float
    approved: bool
    class Config:
        from_attributes = True

class TimesheetSummary(BaseModel):
    employee_id: int
    year: int
    total_hours: float
    total_overtime: float
    days_recorded: int
    standard_day_hours: int

@router.get("/", response_model=List[TimesheetResponse])
def get_all_timesheets(db: Session = Depends(get_db), current_user=Depends(get_current_user), skip: int = 0, limit: int = 100):
    """Get all timesheets for HR admins/project managers, or current user's timesheets otherwise"""
    if current_user.role in ["hr_admin", "project_manager"]:
        return db.query(models.Timesheet).order_by(models.Timesheet.date.desc()).offset(skip).limit(limit).all()
    employee_id = resolve_employee_id(current_user, db)
    if employee_id is not None:
        return db.query(models.Timesheet).filter(models.Timesheet.employee_id == employee_id).order_by(models.Timesheet.date.desc()).offset(skip).limit(limit).all()
    raise HTTPException(status_code=403, detail="No employee record associated with this account")

@router.post("/entry", response_model=TimesheetResponse)
def add_entry(timesheet: TimesheetCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Staff may only add entries for themselves
    if current_user.role == "staff":
        employee_id = resolve_employee_id(current_user, db)
        if employee_id is None or employee_id != timesheet.employee_id:
            raise HTTPException(status_code=403, detail="Staff can only submit their own timesheets")

    db_timesheet = models.Timesheet(**timesheet.dict())
    db.add(db_timesheet)
    db.commit()
    db.refresh(db_timesheet)
    return db_timesheet

@router.get("/employee/{employee_id}", response_model=List[TimesheetResponse])
def get_employee_timesheets(employee_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # HR and managers can view any employee; staff only their own
    if current_user.role in ["hr_admin", "project_manager"]:
        pass
    elif current_user.role == "staff":
        resolved_employee_id = resolve_employee_id(current_user, db)
        if resolved_employee_id is None or resolved_employee_id != employee_id:
            raise HTTPException(status_code=403, detail="Not authorized to view other employee timesheets")
    else:
        raise HTTPException(status_code=403, detail="Not authorized")

    return db.query(models.Timesheet).filter(models.Timesheet.employee_id == employee_id).order_by(models.Timesheet.date.desc()).offset(skip).limit(limit).all()

@router.get("/summary/{employee_id}", response_model=TimesheetSummary)
def get_timesheet_summary(employee_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    year = date.today().year
    # Restrict access: HR/manager or the employee themselves
    if current_user.role in ["hr_admin", "project_manager"]:
        pass
    elif current_user.role == "staff":
        resolved_employee_id = resolve_employee_id(current_user, db)
        if resolved_employee_id is None or resolved_employee_id != employee_id:
            raise HTTPException(status_code=403, detail="Not authorized to view this summary")
    else:
        raise HTTPException(status_code=403, detail="Not authorized")

    total_hours = db.query(func.sum(models.Timesheet.hours_worked)).filter(
        models.Timesheet.employee_id == employee_id,
        models.Timesheet.date >= date(year, 1, 1),
        models.Timesheet.date <= date(year, 12, 31)
    ).scalar() or 0
    total_overtime = db.query(func.sum(models.Timesheet.overtime_hours)).filter(
        models.Timesheet.employee_id == employee_id,
        models.Timesheet.date >= date(year, 1, 1),
        models.Timesheet.date <= date(year, 12, 31)
    ).scalar() or 0
    days_recorded = db.query(func.count(models.Timesheet.id)).filter(
        models.Timesheet.employee_id == employee_id,
        models.Timesheet.date >= date(year, 1, 1),
        models.Timesheet.date <= date(year, 12, 31)
    ).scalar() or 0
    return {
        "employee_id": employee_id,
        "year": year,
        "total_hours": float(total_hours),
        "total_overtime": float(total_overtime),
        "days_recorded": int(days_recorded),
        "standard_day_hours": 8,
    }

@router.put("/{timesheet_id}/approve")
def approve_timesheet(timesheet_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role not in ["hr_admin", "project_manager"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    ts = db.query(models.Timesheet).filter(models.Timesheet.id == timesheet_id).first()
    if not ts:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    ts.approved = True
    db.commit()
    return {"message": "Timesheet approved"}
