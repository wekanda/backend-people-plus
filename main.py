import sys, os
# Ensure backend folder is on sys.path so local bare imports resolve when running as a package module
backend_dir = os.path.dirname(__file__)
sys.path.insert(0, backend_dir)

import database
import models
import auth
import auth_router
import schemas
sys.modules['database'] = database
sys.modules['models'] = models
sys.modules['auth'] = auth
sys.modules['auth_router'] = auth_router
sys.modules['schemas'] = schemas

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from datetime import datetime, date, timedelta
from database import engine, Base, SessionLocal, get_db
from routers import employees, leave, timesheet, appraisal, documents, notifications, upload, recruitment, finance, requisition
from routers import hr_tools, ats, calendar_integration, assessments, reporting, document_generation
from routers import leave_management, employee_documents, document_management, payroll, excel_import
from routers import form_documents as form_documents_router
from routers import smart_alerts, hr_resources, signatures, medical_insurance
from auth_router import router as auth_router
from auth import get_current_user, get_password_hash, verify_password

Base.metadata.create_all(bind=engine)


def _ensure_columns():
    """Add newly introduced columns to existing databases (works for SQLite & Postgres)."""
    stmts = [
        ("employees", "date_of_birth", "DATE"),
        ("employees", "gender", "VARCHAR(16)"),
        ("employees", "passport_photo_url", "VARCHAR"),
        ("employees", "full_photo_url", "VARCHAR"),
        ("employees", "unit", "VARCHAR"),
        ("performance_appraisals", "score", "FLOAT"),
        ("internships", "participant_type", "VARCHAR(32) DEFAULT 'intern'"),
    ]
    with engine.connect() as conn:
        for table, col, ddl in stmts:
            try:
                cols = {r[1] for r in conn.execute(text(f"PRAGMA table_info({table})"))} if "sqlite" in str(engine.url) else None
                if cols is not None and col in cols:
                    continue
                existing = conn.execute(text(
                    "SELECT column_name FROM information_schema.columns WHERE table_name=:t AND column_name=:c"
                ), {"t": table, "c": col}).first() if cols is None else None
                if existing:
                    continue
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} {ddl}"))
                conn.commit()
            except Exception as exc:  # pragma: no cover
                print(f"[migrate] skip {table}.{col}: {exc}")


_ensure_columns()

def initialize_seed_users():
    test_users = [
        {
            "email": "admin@peoplepluse.com",
            "password": "admin123",
            "full_name": "Admin User",
            "role": "hr_admin"
        },
        {
            "email": "manager@peoplepluse.com",
            "password": "manager123",
            "full_name": "Project Manager",
            "role": "project_manager"
        },
        {
            "email": "staff@peoplepluse.com",
            "password": "staff123",
            "full_name": "Staff Member",
            "role": "staff"
        },
        {
            "email": "finance@peoplepluse.com",
            "password": "finance123",
            "full_name": "Finance User",
            "role": "finance"
        },
        {
            "email": "live_staff@peoplepluse.com",
            "password": "LiveStaff123!",
            "full_name": "Live Staff",
            "role": "staff"
        },
        {
            "email": "live_manager@peoplepluse.com",
            "password": "LiveManager123!",
            "full_name": "Live Manager",
            "role": "project_manager"
        },
        {
            "email": "live_admin@peoplepluse.com",
            "password": "LiveAdmin123!",
            "full_name": "Live Admin",
            "role": "hr_admin"
        }
    ]

    db = SessionLocal()
    try:
        # Create or update users
        for user_data in test_users:
            existing = db.query(models.User).filter(models.User.email == user_data["email"]).first()
            if existing:
                try:
                    if not verify_password(user_data["password"], existing.hashed_password):
                        existing.hashed_password = get_password_hash(user_data["password"])
                        existing.full_name = user_data["full_name"]
                        existing.role = user_data["role"]
                        db.add(existing)
                        print(f"Updated password for existing user: {user_data['email']}")
                except Exception:
                    existing.hashed_password = get_password_hash(user_data["password"])
                    existing.full_name = user_data["full_name"]
                    existing.role = user_data["role"]
                    db.add(existing)
                    print(f"Repaired corrupted user record: {user_data['email']}")
            else:
                user = models.User(
                    email=user_data["email"],
                    hashed_password=get_password_hash(user_data["password"]),
                    full_name=user_data["full_name"],
                    role=user_data["role"]
                )
                db.add(user)
                print(f"Created user: {user_data['email']}")
        db.commit()
        
        # Create test employees if none exist
        emp_count = db.query(models.Employee).count()
        if emp_count == 0:
            test_employees = [
                {
                    "file_code": "EMP001",
                    "full_name": "Live Staff",
                    "project": "People Plus Project",
                    "status": "Active",
                    "position": "Staff Member",
                    "contact_number": "0700000001",
                    "location": "Nairobi",
                    "date_of_appointment": date.today() - timedelta(days=180),
                    "contract_start": date.today() - timedelta(days=180),
                    "contract_end": date.today() + timedelta(days=20),
                    "contract_review_date": date.today() + timedelta(days=10),
                    "probation_end": date.today() - timedelta(days=120),
                    "employment_type": "Full-time",
                    "notice_period": "1 month",
                    "photo_url": "https://ui-avatars.com/api/?name=Live+Staff&background=2563eb&color=fff",
                    "missing_app_resume": True,
                },
                {
                    "file_code": "EMP002",
                    "full_name": "Live Manager",
                    "project": "People Plus Project",
                    "status": "Active",
                    "position": "Project Manager",
                    "contact_number": "0700000002",
                    "location": "Nairobi",
                    "date_of_appointment": date.today() - timedelta(days=460),
                    "contract_start": date.today() - timedelta(days=460),
                    "contract_end": date.today() + timedelta(days=45),
                    "contract_review_date": date.today() + timedelta(days=20),
                    "probation_end": date.today() - timedelta(days=360),
                    "employment_type": "Full-time",
                    "notice_period": "2 months",
                    "photo_url": "https://ui-avatars.com/api/?name=Live+Manager&background=1d4ed8&color=fff",
                },
                {
                    "file_code": "EMP003",
                    "full_name": "John Doe",
                    "project": "HR Department",
                    "status": "Active",
                    "position": "HR Officer",
                    "contact_number": "0700000003",
                    "location": "Head Office",
                    "date_of_appointment": date.today() - timedelta(days=210),
                    "contract_start": date.today() - timedelta(days=210),
                    "contract_end": date.today() + timedelta(days=15),
                    "contract_review_date": date.today() + timedelta(days=12),
                    "probation_end": date.today() - timedelta(days=150),
                    "employment_type": "Full-time",
                    "notice_period": "1 month",
                    "photo_url": "https://ui-avatars.com/api/?name=John+Doe&background=1d4ed8&color=fff",
                    "missing_national_id": True,
                    "missing_appointment_letter": True,
                },
                {
                    "file_code": "EMP004",
                    "full_name": "Finance Analyst",
                    "project": "Finance",
                    "status": "Active",
                    "position": "Finance Analyst",
                    "contact_number": "0700000004",
                    "location": "Nairobi",
                    "date_of_appointment": date.today() - timedelta(days=220),
                    "contract_start": date.today() - timedelta(days=220),
                    "contract_end": date.today() + timedelta(days=60),
                    "contract_review_date": date.today() + timedelta(days=30),
                    "probation_end": date.today() - timedelta(days=120),
                    "employment_type": "Full-time",
                    "notice_period": "1 month",
                    "photo_url": "https://ui-avatars.com/api/?name=Finance+Analyst&background=059669&color=fff",
                }
            ]
            for emp_data in test_employees:
                emp = models.Employee(**emp_data)
                db.add(emp)
                print(f"Created employee: {emp_data['file_code']}")
            db.commit()

        # Seed sample job postings
        job_count = db.query(models.JobPosting).count()
        if job_count == 0:
            live_admin_user = db.query(models.User).filter(models.User.email == 'live_admin@peoplepluse.com').first()
            sample_jobs = [
                {
                    'title': 'Software Engineer',
                    'description': 'Develop and maintain web applications for HR and payroll workflows.',
                    'department': 'Engineering',
                    'location': 'Nairobi',
                    'closing_date': date.today() + timedelta(days=20),
                    'status': 'open',
                    'created_by': live_admin_user.id if live_admin_user else None,
                },
                {
                    'title': 'HR Intern',
                    'description': 'Support recruitment campaigns and employee onboarding.',
                    'department': 'Human Resources',
                    'location': 'Remote',
                    'closing_date': date.today() + timedelta(days=14),
                    'status': 'open',
                    'created_by': live_admin_user.id if live_admin_user else None,
                },
                {
                    'title': 'Finance Operations Lead',
                    'description': 'Manage payroll and monthly reporting for employee expenses.',
                    'department': 'Finance',
                    'location': 'Nairobi',
                    'closing_date': date.today() + timedelta(days=30),
                    'status': 'open',
                    'created_by': live_admin_user.id if live_admin_user else None,
                }
            ]
            for j in sample_jobs:
                job = models.JobPosting(**j)
                db.add(job)
            db.commit()

        applicant_count = db.query(models.Applicant).count()
        if applicant_count == 0:
            sample_applicants = [
                {
                    'full_name': 'Amina Yusuf',
                    'email': 'amina.yusuf@example.com',
                    'phone': '0712345678',
                    'source': 'linkedin',
                    'resume_url': 'https://example.com/resume/amina_yusuf.pdf',
                },
                {
                    'full_name': 'David Kimani',
                    'email': 'david.kimani@example.com',
                    'phone': '0722345678',
                    'source': 'referral',
                    'resume_url': 'https://example.com/resume/david_kimani.pdf',
                },
                {
                    'full_name': 'Selina Mwangi',
                    'email': 'selina.mwangi@example.com',
                    'phone': '0732345678',
                    'source': 'career_page',
                    'resume_url': 'https://example.com/resume/selina_mwangi.pdf',
                }
            ]
            for item in sample_applicants:
                db.add(models.Applicant(**item))
            db.commit()

        application_count = db.query(models.Application).count()
        if application_count == 0:
            jobs = db.query(models.JobPosting).all()
            job_map = {job.title: job.id for job in jobs}
            sample_applications = [
                {
                    'job_id': job_map.get('Software Engineer'),
                    'applicant_name': 'Amina Yusuf',
                    'email': 'amina.yusuf@example.com',
                    'resume_url': 'https://example.com/resume/amina_yusuf.pdf',
                    'cover_letter': 'I am excited to bring three years of full-stack experience to your team.',
                    'status': 'screening'
                },
                {
                    'job_id': job_map.get('HR Intern'),
                    'applicant_name': 'David Kimani',
                    'email': 'david.kimani@example.com',
                    'resume_url': 'https://example.com/resume/david_kimani.pdf',
                    'cover_letter': 'I have supported recruitment drives and employee onboarding before.',
                    'status': 'interview'
                },
                {
                    'job_id': job_map.get('Finance Operations Lead'),
                    'applicant_name': 'Selina Mwangi',
                    'email': 'selina.mwangi@example.com',
                    'resume_url': 'https://example.com/resume/selina_mwangi.pdf',
                    'cover_letter': 'I bring strong payroll and reporting experience for modern HR systems.',
                    'status': 'submitted'
                }
            ]
            for application_data in sample_applications:
                db.add(models.Application(**application_data))
            db.commit()

            for app in db.query(models.Application).all():
                if app.status == 'screening':
                    app_stage = models.ApplicationStage(application_id=app.id, stage='screening', status='scored', note='Initial screening complete')
                elif app.status == 'interview':
                    app_stage = models.ApplicationStage(application_id=app.id, stage='interview', status='scheduled', note='Interview scheduled with hiring manager')
                else:
                    app_stage = models.ApplicationStage(application_id=app.id, stage='new', status='submitted', note='New application received')
                db.add(app_stage)
            db.commit()

        internship_count = db.query(models.Internship).count()
        if internship_count == 0:
            mentor_manager = db.query(models.User).filter(models.User.email == 'live_manager@peoplepluse.com').first()
            mentor_admin = db.query(models.User).filter(models.User.email == 'live_admin@peoplepluse.com').first()
            sample_internships = []
            if mentor_manager:
                sample_internships.append({
                    'candidate_name': 'Juma Odhiambo',
                    'email': 'juma.odhiambo@example.com',
                    'start_date': date.today() + timedelta(days=5),
                    'end_date': date.today() + timedelta(days=95),
                    'mentor_id': mentor_manager.id,
                    'status': 'planned',
                    'notes': 'Internship for HR process improvement and onboarding automation.',
                })
            if mentor_admin:
                sample_internships.append({
                    'candidate_name': 'Grace Njeri',
                    'email': 'grace.njeri@example.com',
                    'start_date': date.today() - timedelta(days=10),
                    'end_date': date.today() + timedelta(days=80),
                    'mentor_id': mentor_admin.id,
                    'status': 'in_progress',
                    'notes': 'Finance internship focused on payroll reconciliation and reporting.',
                })
            for internship_data in sample_internships:
                db.add(models.Internship(**internship_data))
            db.commit()

        leave_count = db.query(models.LeaveRequest).count()
        if leave_count == 0:
            emp1 = db.query(models.Employee).filter(models.Employee.file_code == 'EMP001').first()
            emp2 = db.query(models.Employee).filter(models.Employee.file_code == 'EMP002').first()
            sample_leave = []
            if emp1:
                sample_leave.append(models.LeaveRequest(employee_id=emp1.id, start_date=date.today() + timedelta(days=4), end_date=date.today() + timedelta(days=8), days=5, reason='Family travel', type='Annual', status='Pending'))
            if emp2:
                sample_leave.append(models.LeaveRequest(employee_id=emp2.id, start_date=date.today() - timedelta(days=20), end_date=date.today() - timedelta(days=16), days=5, reason='Project handover', type='Sick', status='Approved'))
            for leave_data in sample_leave:
                db.add(leave_data)
            db.commit()

        timesheet_count = db.query(models.Timesheet).count()
        if timesheet_count == 0:
            emp1 = db.query(models.Employee).filter(models.Employee.file_code == 'EMP001').first()
            emp2 = db.query(models.Employee).filter(models.Employee.file_code == 'EMP002').first()
            emp3 = db.query(models.Employee).filter(models.Employee.file_code == 'EMP003').first()
            sample_timesheets = []
            if emp1:
                sample_timesheets.append(models.Timesheet(employee_id=emp1.id, date=date.today() - timedelta(days=1), hours_worked=8, overtime_hours=1, approved=False))
            if emp2:
                sample_timesheets.append(models.Timesheet(employee_id=emp2.id, date=date.today() - timedelta(days=1), hours_worked=9, overtime_hours=0, approved=False))
            if emp3:
                sample_timesheets.append(models.Timesheet(employee_id=emp3.id, date=date.today() - timedelta(days=2), hours_worked=8, overtime_hours=0, approved=True))
            for timesheet_data in sample_timesheets:
                db.add(timesheet_data)
            db.commit()

        payslip_count = db.query(models.Payslip).count()
        if payslip_count == 0:
            employee = db.query(models.Employee).filter(models.Employee.file_code == 'EMP001').first()
            live_admin_user = db.query(models.User).filter(models.User.email == 'live_admin@peoplepluse.com').first()
            if employee:
                p = models.Payslip(
                    employee_id=employee.id,
                    period_start=date.today().replace(day=1),
                    period_end=date.today(),
                    gross_pay=2200.0,
                    tax=330.0,
                    deductions=120.0,
                    net_pay=1750.0,
                    generated_by=live_admin_user.id if live_admin_user else None,
                )
                db.add(p)
            employee2 = db.query(models.Employee).filter(models.Employee.file_code == 'EMP004').first()
            if employee2:
                p2 = models.Payslip(
                    employee_id=employee2.id,
                    period_start=date.today().replace(day=1),
                    period_end=date.today(),
                    gross_pay=2700.0,
                    tax=405.0,
                    deductions=100.0,
                    net_pay=2195.0,
                    generated_by=live_admin_user.id if live_admin_user else None,
                )
                db.add(p2)
            db.commit()

        offer_count = db.query(models.Offer).count()
        if offer_count == 0:
            applicants = db.query(models.Applicant).all()
            if applicants:
                db.add(models.Offer(
                    applicant_id=applicants[0].id,
                    position='Software Engineer',
                    salary=3800.0,
                    start_date=date.today() + timedelta(days=14),
                    status='pending'
                ))
                if len(applicants) > 1:
                    db.add(models.Offer(
                        applicant_id=applicants[1].id,
                        position='HR Intern',
                        salary=3400.0,
                        start_date=date.today() + timedelta(days=7),
                        status='sent'
                    ))
            db.commit()

        background_check_count = db.query(models.BackgroundCheck).count()
        if background_check_count == 0:
            applications = db.query(models.Application).all()
            if applications:
                db.add(models.BackgroundCheck(application_id=applications[0].id, type='standard', status='in_progress', result='Pending review'))
                db.add(models.BackgroundCheck(application_id=applications[1].id, type='basic', status='passed', result='Verified identity and employment history'))
            db.commit()

        audit_count = db.query(models.AuditLog).count()
        if audit_count == 0:
            live_admin_user = db.query(models.User).filter(models.User.email == 'live_admin@peoplepluse.com').first()
            db.add(models.AuditLog(user_id=live_admin_user.id if live_admin_user else None, action='seed_initialized', object_type='system', object_id='0', details='Seed data created'))
            db.commit()

        # Link live_staff, live_manager, finance user to their employees
        live_staff_user = db.query(models.User).filter(models.User.email == "live_staff@peoplepluse.com").first()
        live_manager_user = db.query(models.User).filter(models.User.email == "live_manager@peoplepluse.com").first()
        live_finance_user = db.query(models.User).filter(models.User.email == "finance@peoplepluse.com").first()

        emp1 = db.query(models.Employee).filter(models.Employee.file_code == "EMP001").first()
        emp2 = db.query(models.Employee).filter(models.Employee.file_code == "EMP002").first()
        emp4 = db.query(models.Employee).filter(models.Employee.file_code == "EMP004").first()

        if live_staff_user and emp1:
            live_staff_user.employee_id = emp1.id
            db.add(live_staff_user)
            print(f"Linked live_staff to employee id {emp1.id}")

        if live_manager_user and emp2:
            live_manager_user.employee_id = emp2.id
            db.add(live_manager_user)
            print(f"Linked live_manager to employee id {emp2.id}")

        if live_finance_user and emp4:
            live_finance_user.employee_id = emp4.id
            db.add(live_finance_user)
            print(f"Linked finance user to employee id {emp4.id}")

        db.commit()
    except Exception as e:
        print(f"Seed initialization warning: {e}")
        db.rollback()
    finally:
        db.close()

initialize_seed_users()

# Ensure new SQLite columns exist when the app schema evolves.
def ensure_schema_columns():
    db_url = str(engine.url)
    if "sqlite" in db_url:
        try:
            with engine.connect() as conn:
                result = conn.execute(text("PRAGMA table_info(employees)"))
                columns = [row[1] for row in result]
                if 'gender' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN gender VARCHAR'))
                if 'location' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN location VARCHAR'))
                if 'photo_url' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN photo_url VARCHAR'))
                if 'driving_permit_number' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN driving_permit_number VARCHAR'))
                if 'emergency_contact_relationship' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN emergency_contact_relationship VARCHAR'))
                if 'bank_account_holder_name' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN bank_account_holder_name VARCHAR'))
                if 'education_level' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN education_level VARCHAR'))
                if 'locker' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN locker VARCHAR'))
                if 'notice_period' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN notice_period VARCHAR'))
                if 'contract_review_date' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN contract_review_date DATE'))
                if 'probation_end' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN probation_end DATE'))
                if 'missing_recruitment_notes' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN missing_recruitment_notes BOOLEAN DEFAULT 0'))
                if 'missing_staff_id_form' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN missing_staff_id_form BOOLEAN DEFAULT 0'))
                if 'missing_performance_appraisals' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN missing_performance_appraisals BOOLEAN DEFAULT 0'))
                if 'missing_policy_declaration' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN missing_policy_declaration BOOLEAN DEFAULT 0'))
                if 'missing_end_of_contract_notice' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN missing_end_of_contract_notice BOOLEAN DEFAULT 0'))
                if 'missing_medical_insurance_form' not in columns:
                    conn.execute(text('ALTER TABLE employees ADD COLUMN missing_medical_insurance_form BOOLEAN DEFAULT 0'))

                result = conn.execute(text("PRAGMA table_info(employee_documents)"))
                doc_columns = [row[1] for row in result]
                if 'approved' not in doc_columns:
                    conn.execute(text('ALTER TABLE employee_documents ADD COLUMN approved BOOLEAN DEFAULT 0'))
                    conn.execute(text("UPDATE employee_documents SET approved = 1 WHERE approval_status = 'approved'"))
                conn.commit()
        except Exception as e:
            print(f"SQLite schema check warning: {e}")

try:
    ensure_schema_columns()
except Exception as e:
    print(f"Schema initialization warning: {e}")

app = FastAPI(title="PEOPLE PLUSE API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(employees.router)
app.include_router(leave.router)
app.include_router(timesheet.router)
app.include_router(appraisal.router)
app.include_router(documents.router)
app.include_router(notifications.router)
app.include_router(upload.router)
app.include_router(recruitment.router)
app.include_router(hr_tools.router)
app.include_router(finance.router)
app.include_router(requisition.router)
app.include_router(ats.router)
app.include_router(calendar_integration.router)
app.include_router(assessments.router)
app.include_router(reporting.router)
app.include_router(document_generation.router)
app.include_router(leave_management.router)
app.include_router(employee_documents.router)
app.include_router(document_management.router)
app.include_router(payroll.router)
app.include_router(excel_import.router)
app.include_router(form_documents_router.router)
app.include_router(smart_alerts.router)
app.include_router(hr_resources.router)
app.include_router(signatures.router)
app.include_router(medical_insurance.router)

@app.get("/health")
@app.get("/api/health")
def root():
    return {"message": "PEOPLE PLUSE API running", "status": "ok"}

@app.get("/api/debug/schema")
def debug_schema(db: Session = Depends(get_db)):
    """Debug endpoint to check database schema"""
    try:
        # Get all table names
        from sqlalchemy import text
        result = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result]
        
        schema_info = {}
        for table in tables:
            result = db.execute(text(f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = '{table}' ORDER BY ordinal_position"))
            schema_info[table] = [{"name": row[0], "type": row[1], "nullable": row[2]} for row in result]
        
        return {"tables": tables, "schema": schema_info}
    except Exception as e:
        return {"error": str(e)}

def _dashboard_extended(db: Session, today):
    """Compute the expanded People Plus Dashboard analytics:

    Analytics, Performance Analysis, Pipeline and Reports catalogs that power
    the Dashboard, plus a Smart-Alerts summary with all alert categories.
    """
    employees = db.query(models.Employee).all()
    total = len(employees)

    def _status_count(pred):
        return sum(1 for e in employees if pred(e.status))

    active = _status_count(lambda s: (s or "").lower() in ("active", "on duty", "probation"))
    recess = _status_count(lambda s: "recess" in (s or "").lower())
    exited = _status_count(lambda s: (s or "").lower() in ("inactive", "exited", "terminated", "left"))

    # Employment type -> permanent vs temporary / service level agreement (SLA)
    permanent = sum(1 for e in employees if e.employment_type and "permanent" in e.employment_type.lower())
    temporary = sum(1 for e in employees if any(
        kw in (e.employment_type or "").lower() for kw in ("temporary", "sla", "service level", "casual", "contract")))
    if temporary == 0:
        unknown = [e for e in employees if not e.employment_type]
        temporary = len(unknown)

    turnover = (exited / total * 100) if total else 0

    gender_breakdown = {}
    for e in employees:
        key = (e.gender or "").strip().title() or "Unspecified"
        gender_breakdown[key] = gender_breakdown.get(key, 0) + 1

    by_project = {}
    by_unit = {}
    for e in employees:
        p = e.project or "Unassigned"
        by_project[p] = by_project.get(p, 0) + 1
        u = e.unit or (e.location or "Unassigned Unit")
        by_unit[u] = by_unit.get(u, 0) + 1
# ---- Performance analysis (per unit, per staff, per project) ----
    appraisals = db.query(models.PerformanceAppraisal).all()
    perf_unit, perf_staff, perf_project = {}, [], []
    for a in appraisals:
        emp = next((x for x in employees if x.id == a.employee_id), None)
        score = a.score or 0
        if emp:
            perf_staff.append({"name": emp.full_name, "file_code": emp.file_code, "score": score,
                               "unit": emp.unit or emp.project or "Unassigned"})
    avg = (sum(a.score or 0 for a in appraisals) / len(appraisals)) if appraisals else 0
    for e in employees:
        u = e.unit or (e.project or "Unassigned Unit")
        entry = perf_unit.setdefault(u, {"staff": 0, "score_total": 0.0, "count": 0})
        entry["staff"] += 1
        scores = [a.score or 0 for a in appraisals if a.employee_id == e.id]
        if scores:
            entry["score_total"] += sum(scores)
            entry["count"] += len(scores)
    for p in sorted(by_project):
        p_emps = [e for e in employees if (e.project or "Unassigned") == p]
        p_scores = [a.score or 0 for a in appraisals if a.employee_id in {x.id for x in p_emps}]
        perf_project.append({"project": p, "score": round(sum(p_scores) / len(p_scores), 2) if p_scores else round(avg, 2),
                             "staff": len(p_emps), "rated": len(p_scores)})

    # ---- Pipeline ----
    vacancies = db.query(models.JobPosting).filter(
        func.lower(models.JobPosting.status).in_(("open", "active", "draft"))).count()
    applications = db.query(models.Application).count()
    interns = 0
    volunteers = 0
    for it in db.query(models.Internship).all():
        if (getattr(it, "participant_type", None) or "intern").lower() == "volunteer":
            volunteers += 1
        else:
            interns += 1
    open_vacancies = db.query(models.JobPosting).filter(
        func.lower(models.JobPosting.status) == "open").count()

    # ---- Smart Alerts summary (12 categories) ----
    thirty_days_later = today + timedelta(days=30)
    birthdays = sum(1 for e in employees if e.date_of_birth)
    staff_anniversaries = sum(1 for e in employees if (e.contract_start or e.date_of_appointment))
    company_anniversaries = birthdays  # anniversary cohort count
    employee_of_month = next((e.full_name for e in employees if e.status == "Active"), None)
    missing_docs = sum(1 for e in employees if (
        e.missing_app_resume or e.missing_national_id or e.missing_appointment_letter
        or e.missing_academic_docs or e.missing_recruitment_notes or e.missing_staff_id_form
        or e.missing_performance_appraisals or e.missing_policy_declaration or e.missing_end_of_contract_notice))
    end_of_project = sum(1 for e in employees if e.contract_end and e.project)
    contract_expiring = db.query(models.Employee).filter(
        models.Employee.contract_end.between(today, thirty_days_later)).count()
    probation_period = sum(1 for e in employees if e.probation_end and today <= e.probation_end <= thirty_days_later)
    contracts_to_review = sum(1 for e in employees if e.contract_review_date and today <= e.contract_review_date <= thirty_days_later)
    leave_requests = db.query(models.LeaveRequest).filter(models.LeaveRequest.status == "Pending").count()
    retirement = sum(1 for e in employees if e.date_of_birth and (today.year - e.date_of_birth.year) >= 58)
    registration = sum(1 for e in employees if e.date_of_appointment and (today - e.date_of_appointment).days <= 30)

    return {
        "analytics": {
            "total_staff": total,
            "active_staff": active,
            "permanent_staff": permanent,
            "temporary_staff": temporary,
            "on_recess": recess,
            "exited_staff": exited,
            "turnover_rate_percent": round(turnover, 2),
            "gender_breakdown": gender_breakdown,
            "organizational": total,
            "per_project": by_project,
            "per_unit": by_unit,
        },
        "performance_analysis": {
            "organizational_rating": round(avg, 2),
            "per_unit": {u: round(v["score_total"] / v["count"], 2) if v["count"] else round(avg, 2)
                         for u, v in perf_unit.items()},
            "per_staff": perf_staff,
            "per_project": perf_project,
        },
        "pipeline": {
            "vacancies": vacancies,
            "open_vacancies": open_vacancies,
            "applications": applications,
            "volunteer_requests": volunteers,
            "internship_requests": interns,
            "job_description_sections": [
                "Job information", "Job purpose", "Key responsibilities and duties",
                "Qualifications and experience", "Skills and competencies",
                "Key performance indicators", "Working conditions", "Compliance",
                "Safeguarding & compliance responsibilities",
            ],
        },

"reports": {
            "report_types": [
                "Incident report", "Performance review report", "Budget report",
                "Recruitment report", "Interview report", "Internship report",
                "Volunteer report", "Disciplinary report", "Training report",
                "Project report", "Unit / Department report",
            ],
            "report_durations": [
                {"name": "Monthly", "frequency": "Done every month"},
                {"name": "Quarterly", "frequency": "Done every 3 months"},
                {"name": "Semi-annual", "frequency": "Done every 6 months"},
                {"name": "Annual", "frequency": "Once per year"},
                {"name": "Final", "frequency": "Done when the project is closing"},
            ],
        },
        "smart_alerts": {
            "birthdays": birthdays,
            "company_anniversaries": company_anniversaries,
            "staff_anniversaries": staff_anniversaries,
            "employee_of_the_month": employee_of_month,
            "missing_docs": missing_docs,
            "end_of_project_notice": end_of_project,
            "contract_expiring": contract_expiring,
            "probation_period": probation_period,
            "contracts_to_review": contracts_to_review,
            "leave_requests_approvals": leave_requests,
            "retirement": retirement,
            "registration": registration,
        },
    }

@app.get("/api/dashboard")
def dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    total_staff = db.query(models.Employee).count()
    active_staff = db.query(models.Employee).filter(models.Employee.status == "Active").count()
    
    # Contracts expiring in next 30 days
    today = datetime.now().date()
    thirty_days_later = today + timedelta(days=30)
    expiring_soon = db.query(models.Employee).filter(
        models.Employee.contract_end.between(today, thirty_days_later)
    ).count()
    
    # Missing documents
    missing_docs = db.query(models.Employee).filter(
        (models.Employee.missing_app_resume == True) |
        (models.Employee.missing_national_id == True) |
        (models.Employee.missing_appointment_letter == True)
    ).count()

    project_count = db.query(models.Employee.project).distinct().count()
    location_count = db.query(models.Employee.location).filter(models.Employee.location != None).distinct().count()
    
    # Payroll-related summary (using timesheet data)
    year = today.year
    total_hours = db.query(func.sum(models.Timesheet.hours_worked + models.Timesheet.overtime_hours)).filter(
        models.Timesheet.date >= date(year, 1, 1),
        models.Timesheet.date <= date(year, 12, 31)
    ).scalar() or 0
    pending_timesheet_approvals = db.query(models.Timesheet).filter(models.Timesheet.approved == False).count()
    pending_leave_approvals = db.query(models.LeaveRequest).filter(models.LeaveRequest.status == "Pending").count()
    unread_notifications = db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id,
        models.Notification.read == False
    ).count()

    # Get list of expiring contracts
    expiring_contracts = db.query(models.Employee).filter(
        models.Employee.contract_end.between(today, thirty_days_later)
    ).all()
    
    expiring_list = [
        {
            "id": emp.id,
            "full_name": emp.full_name,
            "file_code": emp.file_code,
            "contract_end": str(emp.contract_end),
            "project": emp.project,
            "position": emp.position,
            "status": emp.status,
            "contact_number": emp.contact_number,
            "location": emp.location,
            "photo_url": emp.photo_url,
            "missing_app_resume": emp.missing_app_resume,
            "missing_appointment_letter": emp.missing_appointment_letter,
            "missing_academic_docs": emp.missing_academic_docs,
            "missing_national_id": emp.missing_national_id,
        }
        for emp in expiring_contracts
    ]

    featured_employee = expiring_list[0] if expiring_list else None
    
    _ext = _dashboard_extended(db, today)
    return {
        "total_staff": total_staff,
        "active_staff": active_staff,
        "contracts_expiring_soon": expiring_soon,
        "staff_with_missing_docs": missing_docs,
        "project_count": project_count,
        "location_count": location_count,
        "year_to_date_hours": float(total_hours),
        "pending_leave_approvals": pending_leave_approvals,
        "pending_timesheet_approvals": pending_timesheet_approvals,
        "unread_notifications": unread_notifications,
        "expiring_contracts": expiring_list,
        "featured_employee": featured_employee,
        **_ext
    }

# Mount static files LAST so API routes take precedence
static_dir = os.path.join(os.path.dirname(__file__), "static")
try:
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

