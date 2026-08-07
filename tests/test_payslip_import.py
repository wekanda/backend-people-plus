from fastapi.testclient import TestClient
from backend.main import app
import openpyxl
import io
import uuid
from pathlib import Path
from datetime import date

client = TestClient(app)


def make_sample_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['file code', 'period start', 'period end', 'gross_pay', 'tax', 'deductions'])
    ws.append(['EMP001', '2023-01-01', '2023-01-31', 2000, 200, 50])
    bio = io.BytesIO()
    wb.save(bio)
    bio.seek(0)
    return bio


def test_payslip_upload_unauthenticated():
    res = client.post('/upload/payslips_excel', files={'file': ('payslips.xlsx', make_sample_excel(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')})
    assert res.status_code in (401, 403)


def test_form_style_payslip_template_is_reported_clearly():
    from backend.main import models as backend_models
    from backend.database import SessionLocal
    from backend.auth import create_access_token, get_password_hash

    db = SessionLocal()
    try:
        unique_email = f'demo.hr+{uuid.uuid4().hex[:8]}@example.com'
        user = backend_models.User(
            email=unique_email,
            hashed_password=get_password_hash('demo123'),
            full_name='HR Admin Demo',
            role='hr_admin',
            employee_id=None,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token({'sub': user.id})
        payload = Path('excel/PAYSLIP.xlsx').read_bytes()
        res = client.post(
            '/upload/payslips_excel',
            files={'file': ('PAYSLIP.xlsx', payload, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')},
            headers={'Authorization': f'Bearer {token}'},
        )

        assert res.status_code == 200
        payload = res.json()
        assert payload['imported'] == 0
        assert 'form-style' in ' '.join(payload['errors']).lower()
    finally:
        db.close()


def test_payslips_return_for_user_with_matching_employee_name():
    from backend.main import models as backend_models
    from backend.database import SessionLocal
    from backend.auth import create_access_token, get_password_hash

    db = SessionLocal()
    try:
        import uuid
        unique_code = f'EMP{uuid.uuid4().hex[:6].upper()}'
        unique_name = f'Demo Staff {uuid.uuid4().hex[:4]}'
        employee = backend_models.Employee(
            file_code=unique_code,
            full_name=unique_name,
            project='Test Project',
            status='Active',
            position='Tester',
        )
        db.add(employee)
        db.flush()

        unique_email = f'demo.staff2+{uuid.uuid4().hex[:8]}@example.com'
        user = backend_models.User(
            email=unique_email,
            hashed_password=get_password_hash('demo123'),
            full_name=unique_name,
            role='staff',
            employee_id=None,
        )
        db.add(user)
        db.flush()

        db.add(backend_models.Payslip(
            employee_id=employee.id,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            gross_pay=1500.0,
            tax=200.0,
            deductions=50.0,
            net_pay=1250.0,
            generated_by=user.id,
        ))
        db.commit()

        token = create_access_token({'sub': user.id})
        res = client.get('/finance/payslips', headers={'Authorization': f'Bearer {token}'})

        assert res.status_code == 200
        data = res.json()
        assert len(data) == 1
        assert data[0]['employee_id'] == employee.id
    finally:
        db.close()


# Note: authenticated test requires token; manual integration test recommended
