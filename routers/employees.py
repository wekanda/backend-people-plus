from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel, ConfigDict
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from datetime import date
from database import get_db
import models
from auth import get_current_user, check_employee_access, require_role
from typing import List

router = APIRouter(prefix="/api/employees", tags=["employees"])

class EmployeeCreate(BaseModel):
    file_code: str
    full_name: str
    project: str
    status: str = "Active"
    position: str | None = None
    contact_number: str | None = None
    location: str | None = None
    photo_url: str | None = None
    locker: str | None = None
    date_of_appointment: date | None = None
    contract_start: date | None = None
    contract_end: date | None = None
    contract_review_date: date | None = None
    probation_end: date | None = None
    employment_type: str | None = None
    notice_period: str | None = None
    national_id_number: str | None = None
    passport_number: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    date_of_birth: date | None = None
    marital_status: str | None = None
    bank_name: str | None = None
    bank_account_number: str | None = None
    education_level: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    personal_email: str | None = None

class EmployeeUpdate(BaseModel):
    full_name: str | None = None
    status: str | None = None
    position: str | None = None
    contact_number: str | None = None
    location: str | None = None
    photo_url: str | None = None
    contract_end: date | None = None
    missing_app_resume: bool | None = None
    missing_appointment_letter: bool | None = None
    missing_academic_docs: bool | None = None
    missing_national_id: bool | None = None
    national_id_number: str | None = None
    passport_number: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    date_of_birth: date | None = None
    marital_status: str | None = None
    bank_name: str | None = None
    bank_account_number: str | None = None
    education_level: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    personal_email: str | None = None

class EmployeeResponse(BaseModel):
    id: int
    file_code: str
    full_name: str
    project: str | None = None
    status: str | None = None
    position: str | None = None
    contact_number: str | None = None
    location: str | None = None
    photo_url: str | None = None
    employment_type: str | None = None
    contract_end: date | None = None
    national_id_number: str | None = None
    passport_number: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    date_of_birth: date | None = None
    marital_status: str | None = None
    bank_name: str | None = None
    bank_account_number: str | None = None
    education_level: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    personal_email: str | None = None
    model_config = ConfigDict(from_attributes=True)

def resolve_or_create_employee_profile(current_user, db: Session):
    employee = None
    if current_user.employee_id is not None:
        employee = db.query(models.Employee).filter(models.Employee.id == current_user.employee_id).first()
    if not employee and current_user.email:
        employee = db.query(models.Employee).filter(models.Employee.personal_email == current_user.email).first()

    if not employee and current_user.full_name:
        employee = db.query(models.Employee).filter(models.Employee.full_name == current_user.full_name).first()
        if employee:
            employee.personal_email = current_user.email
            db.add(employee)
            current_user.employee_id = employee.id
            db.add(current_user)
            db.commit()

    if not employee:
        file_code = f"AUTO-{current_user.id}"
        suffix = 1
        while db.query(models.Employee).filter(models.Employee.file_code == file_code).first():
            suffix += 1
            file_code = f"AUTO-{current_user.id}-{suffix}"

        employee = models.Employee(
            file_code=file_code,
            full_name=current_user.full_name or current_user.email.split('@')[0],
            project='Unknown',
            status='Active',
            position='Staff',
            personal_email=current_user.email,
            contact_number='',
            location='',
            locker='',
            date_of_appointment=date.today(),
            contract_start=date.today(),
            contract_end=date.today(),
            contract_review_date=date.today(),
            probation_end=date.today(),
            employment_type='Full-time',
            notice_period='N/A',
            photo_url=None,
        )
        db.add(employee)
        db.flush()
        current_user.employee_id = employee.id
        db.add(current_user)
        db.commit()
        db.refresh(employee)

    return employee

@router.get("/me", response_model=EmployeeResponse)
def get_my_profile(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    employee = resolve_or_create_employee_profile(current_user, db)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee profile not found")
    return employee

@router.get("/", response_model=List[EmployeeResponse])
def list_employees(skip: int = 0, limit: int = 100, status: str = None, project: str = None, personal_email: str = None,
                   db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    query = db.query(models.Employee)
    if personal_email:
        query = query.filter(models.Employee.personal_email == personal_email)
    if current_user.role == "project_manager":
        manager = db.query(models.Employee).filter(models.Employee.id == current_user.employee_id).first()
        if manager and manager.project:
            query = query.filter(models.Employee.project == manager.project)
        else:
            query = query.filter(models.Employee.id == -1)
    elif current_user.role == "staff":
        employee = None
        if current_user.employee_id is not None:
            employee = db.query(models.Employee).filter(models.Employee.id == current_user.employee_id).first()
        if not employee:
            employee = db.query(models.Employee).filter(models.Employee.personal_email == current_user.email).first()
        if employee:
            query = query.filter(models.Employee.id == employee.id)
        else:
            raise HTTPException(status_code=403, detail="Access denied")

    if status:
        query = query.filter(models.Employee.status == status)
    if project:
        query = query.filter(models.Employee.project == project)
    return query.offset(skip).limit(limit).all()

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not check_employee_access(current_user, employee_id, db):
        raise HTTPException(status_code=403, detail="Access denied")
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.post("/", response_model=EmployeeResponse)
@require_role("hr_admin")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    existing = db.query(models.Employee).filter(models.Employee.file_code == employee.file_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="File code already exists")
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if current_user.role != "hr_admin" and current_user.employee_id != employee_id:
        raise HTTPException(status_code=403, detail="Access denied")

    for field, value in employee.dict(exclude_unset=True).items():
        setattr(db_employee, field, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.post("/{employee_id}/photo")
async def upload_employee_photo(employee_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not check_employee_access(current_user, employee_id, db):
        raise HTTPException(status_code=403, detail="Access denied")

    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    upload_dir = Path("uploads/profile_pictures")
    upload_dir.mkdir(parents=True, exist_ok=True)
    extension = Path(file.filename or "profile.jpg").suffix.lower() or ".jpg"
    filename = f"{employee_id}_{uuid4().hex}{extension}"
    destination = upload_dir / filename
    contents = await file.read()
    destination.write_bytes(contents)

    employee.photo_url = f"/uploads/profile_pictures/{filename}"
    db.commit()
    db.refresh(employee)
    return {"message": "Profile photo uploaded", "photo_url": employee.photo_url}

@router.delete("/{employee_id}")
@require_role("hr_admin")
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted"}
