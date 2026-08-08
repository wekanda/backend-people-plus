from fastapi.testclient import TestClient
from backend.main import app
from backend.auth import create_access_token, get_password_hash
from backend.database import SessionLocal
from backend.main import models as backend_models

client = TestClient(app)


def create_hr_user(db):
    user = backend_models.User(
        email='test.hr.user@example.com',
        hashed_password=get_password_hash('test1234'),
        full_name='Test HR User',
        role='hr_admin'
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_application(db):
    application = backend_models.Application(
        job_id=None,
        applicant_name='Test Candidate',
        email='test.candidate@example.com',
        resume_url='https://example.com/resume.pdf',
        cover_letter='I am interested in this role.',
        status='submitted'
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def test_hr_offer_generation_and_list():
    db = SessionLocal()
    try:
        user = db.query(backend_models.User).filter(backend_models.User.email == 'test.hr.user@example.com').first()
        if not user:
            user = create_hr_user(db)

        application = create_application(db)
        token = create_access_token({'sub': user.id})
        headers = {'Authorization': f'Bearer {token}'}

        payload = {
            'application_id': application.id,
            'salary': 8500.0,
            'currency': 'USD',
            'terms': '12-month contract with flexible benefits'
        }

        create_response = client.post('/hr/offer/generate', json=payload, headers=headers)
        assert create_response.status_code == 200, create_response.text
        offer = create_response.json()
        assert offer['application_id'] == application.id
        assert offer['salary'] == 8500.0
        assert offer['currency'] == 'USD'
        assert offer['terms'] == '12-month contract with flexible benefits'

        list_response = client.get('/hr/offers', headers=headers)
        assert list_response.status_code == 200, list_response.text
        offers = list_response.json()
        assert any(o['id'] == offer['id'] for o in offers)
    finally:
        db.close()


def test_background_check_creation_and_list():
    db = SessionLocal()
    try:
        user = db.query(backend_models.User).filter(backend_models.User.email == 'test.hr.user@example.com').first()
        assert user is not None
        application = db.query(backend_models.Application).filter(backend_models.Application.status == 'submitted').order_by(backend_models.Application.id.desc()).first()
        assert application is not None

        token = create_access_token({'sub': user.id})
        headers = {'Authorization': f'Bearer {token}'}

        payload = {
            'application_id': application.id,
            'type': 'standard'
        }

        create_response = client.post('/hr/background/check', json=payload, headers=headers)
        assert create_response.status_code == 200, create_response.text
        check = create_response.json()
        assert check['application_id'] == application.id
        assert check['type'] == 'standard'

        list_response = client.get('/hr/background_checks', headers=headers)
        assert list_response.status_code == 200, list_response.text
        checks = list_response.json()
        assert any(c['id'] == check['id'] for c in checks)
    finally:
        db.close()


def test_hr_interview_crud():
    db = SessionLocal()
    try:
        user = db.query(backend_models.User).filter(backend_models.User.email == 'test.hr.user@example.com').first()
        if not user:
            user = create_hr_user(db)

        application = db.query(backend_models.Application).filter(backend_models.Application.status == 'submitted').order_by(backend_models.Application.id.desc()).first()
        if not application:
            application = create_application(db)

        token = create_access_token({'sub': user.id})
        headers = {'Authorization': f'Bearer {token}'}

        payload = {
            'application_id': application.id,
            'candidate_name': 'Interview Candidate',
            'position': 'HR Specialist',
            'interviewer': 'Jane Doe',
            'notes': 'Initial screening interview',
            'date': '2026-08-10',
            'time': '14:30',
            'duration_minutes': 45,
            'location': 'Conference Room 1',
            'status': 'scheduled'
        }

        create_response = client.post('/hr/interviews', json=payload, headers=headers)
        assert create_response.status_code == 200, create_response.text
        interview = create_response.json()
        assert interview['application_id'] == application.id
        assert interview['candidate_name'] == 'Interview Candidate'
        assert interview['position'] == 'HR Specialist'
        assert interview['interviewer'] == 'Jane Doe'
        assert interview['date'] == '2026-08-10'
        assert interview['time'] == '14:30'
        assert interview['location'] == 'Conference Room 1'

        list_response = client.get('/hr/interviews', headers=headers)
        assert list_response.status_code == 200, list_response.text
        interviews = list_response.json()
        assert any(i['id'] == interview['id'] for i in interviews)

        delete_response = client.delete(f"/hr/interviews/{interview['id']}", headers=headers)
        assert delete_response.status_code == 200, delete_response.text
        assert delete_response.json().get('status') == 'deleted'

        list_after_delete = client.get('/hr/interviews', headers=headers)
        assert list_after_delete.status_code == 200, list_after_delete.text
        interviews_after = list_after_delete.json()
        assert all(i['id'] != interview['id'] for i in interviews_after)
    finally:
        db.close()
