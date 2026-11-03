from fastapi.testclient import TestClient

from main import app
from database import SessionLocal
from auth import create_access_token, get_password_hash
import models

client = TestClient(app)


def _make_user_and_employee(role="staff"):
    db = SessionLocal()
    try:
        employee = models.Employee(
            file_code=f"EMP{__import__('uuid').uuid4().hex[:8].upper()}",
            full_name="Demo Employee",
            project="Test Project",
            status="Active",
            position="Officer",
            contact_number="12345",
            location="Nairobi",
        )
        db.add(employee)
        db.flush()

        employee_id = employee.id
        user = models.User(
            email=f"{role}.{__import__('uuid').uuid4().hex[:8]}@example.com",
            hashed_password=get_password_hash("demo123"),
            full_name="Demo Employee",
            role=role,
            employee_id=employee_id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user, employee_id
    finally:
        db.close()


def test_employee_signature_upload_and_verification_flow():
    staff_user, employee_id = _make_user_and_employee(role="staff")
    admin_user, _ = _make_user_and_employee(role="hr_admin")
    staff_token = create_access_token({"sub": staff_user.id})
    admin_token = create_access_token({"sub": admin_user.id})

    upload = client.post(
        f"/api/signatures/employee/{employee_id}",
        headers={"Authorization": f"Bearer {staff_token}"},
        files={"file": ("signature.png", b"test-signature", "image/png")},
        data={"signature_type": "primary"},
    )
    assert upload.status_code == 200, upload.text
    payload = upload.json()
    assert payload["employee_id"] == employee_id
    assert payload["signature_type"] == "primary"
    assert payload["status"] == "Pending Verification"

    list_resp = client.get(
        f"/api/signatures/employee/{employee_id}",
        headers={"Authorization": f"Bearer {staff_token}"},
    )
    assert list_resp.status_code == 200, list_resp.text
    data = list_resp.json()
    assert len(data["items"]) >= 1

    verify = client.post(
        f"/api/signatures/employee/{employee_id}/verify",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"signature_id": payload["id"], "status": "verified"},
    )
    assert verify.status_code == 200, verify.text
    assert verify.json()["status"] == "verified"
