from fastapi.testclient import TestClient
from backend.main import app
from backend.auth import create_access_token, get_password_hash
from backend.database import SessionLocal
from backend.main import models as backend_models

client = TestClient(app)


def test_current_user_profile_returns_matching_employee():
    db = SessionLocal()
    try:
        import uuid
        unique_code = f'EMP{uuid.uuid4().hex[:6].upper()}'
        unique_name = f'Demo Profile {uuid.uuid4().hex[:4]}'

        employee = backend_models.Employee(
            file_code=unique_code,
            full_name=unique_name,
            project='Test Project',
            status='Active',
            position='Tester',
            contact_number='12345',
            location='Nairobi',
        )
        db.add(employee)
        db.flush()

        user = backend_models.User(
            email=f'profile.{uuid.uuid4().hex[:8]}@example.com',
            hashed_password=get_password_hash('demo123'),
            full_name=unique_name,
            role='staff',
            employee_id=None,
        )
        db.add(user)
        db.commit()

        token = create_access_token({'sub': user.id})
        res = client.get('/api/employees/me', headers={'Authorization': f'Bearer {token}'})

        assert res.status_code == 200
        assert res.json()['id'] == employee.id
        assert res.json()['full_name'] == unique_name
    finally:
        db.close()
