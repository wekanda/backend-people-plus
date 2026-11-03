from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from auth import create_access_token, get_password_hash
from database import SessionLocal
from main import app
import models


client = TestClient(app)


def test_update_profile_syncs_linked_employee_name_and_email():
    db = SessionLocal()
    user_id = None
    employee_id = None
    original_email = f"profile-{uuid4().hex}@example.com"
    updated_email = f"updated-{uuid4().hex}@example.com"
    try:
        employee = models.Employee(
            file_code=f"PROFILE-{uuid4().hex[:8].upper()}",
            full_name="Before Update",
            personal_email=original_email,
            project="Test Project",
            status="Active",
        )
        db.add(employee)
        db.flush()
        employee_id = employee.id

        user = models.User(
            email=original_email,
            hashed_password=get_password_hash("demo123"),
            full_name="Before Update",
            role="staff",
            employee_id=employee_id,
        )
        db.add(user)
        db.commit()
        user_id = user.id
        token = create_access_token({"sub": user_id})

        response = client.put(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            json={"full_name": "After Update", "email": updated_email},
        )

        assert response.status_code == 200, response.text
        assert response.json()["full_name"] == "After Update"
        db.expire_all()
        updated_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).one()
        assert updated_employee.full_name == "After Update"
        assert updated_employee.personal_email == updated_email
    finally:
        if user_id is not None:
            db.query(models.User).filter(models.User.id == user_id).delete()
        if employee_id is not None:
            db.query(models.Employee).filter(models.Employee.id == employee_id).delete()
        db.commit()
        db.close()


def test_profile_photo_uploads_persist_and_serve():
    db = SessionLocal()
    user_id = None
    employee_id = None
    uploaded_files = []
    try:
        employee = models.Employee(
            file_code=f"PHOTO-{uuid4().hex[:8].upper()}",
            full_name="Photo Test Employee",
            project="Test Project",
            status="Active",
        )
        db.add(employee)
        db.flush()
        employee_id = employee.id

        user = models.User(
            email=f"photo-{uuid4().hex}@example.com",
            hashed_password=get_password_hash("demo123"),
            full_name="Photo Test Employee",
            role="staff",
            employee_id=employee_id,
        )
        db.add(user)
        db.commit()
        user_id = user.id
        token = create_access_token({"sub": user_id})
        headers = {"Authorization": f"Bearer {token}"}
        image_bytes = b"test-image-content"

        for kind in ("passport", "full"):
            response = client.post(
                f"/api/employees/{employee_id}/photos/{kind}",
                headers=headers,
                files={"file": (f"{kind}.jpg", image_bytes, "image/jpeg")},
            )
            assert response.status_code == 200, response.text
            image_url = response.json()[f"{kind}_photo_url"]
            assert image_url.startswith("/uploads/profile_pictures/")
            uploaded_files.append(Path(__file__).resolve().parents[1] / image_url.lstrip("/"))

            image_response = client.get(image_url)
            assert image_response.status_code == 200
            assert image_response.content == image_bytes

        db.expire_all()
        updated_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).one()
        assert updated_employee.passport_photo_url.endswith(".jpg")
        assert updated_employee.full_photo_url.endswith(".jpg")
    finally:
        for uploaded_file in uploaded_files:
            uploaded_file.unlink(missing_ok=True)
        if user_id is not None:
            db.query(models.User).filter(models.User.id == user_id).delete()
        if employee_id is not None:
            db.query(models.Employee).filter(models.Employee.id == employee_id).delete()
        db.commit()
        db.close()


def test_signature_and_hr_stamp_uploads_serve():
    db = SessionLocal()
    user_id = None
    uploaded_files = []
    try:
        user = models.User(
            email=f"identity-{uuid4().hex}@example.com",
            hashed_password=get_password_hash("demo123"),
            full_name="Identity Test Admin",
            role="hr_admin",
        )
        db.add(user)
        db.commit()
        user_id = user.id
        headers = {"Authorization": f"Bearer {create_access_token({'sub': user_id})}"}
        image_bytes = b"test-identity-image"

        signature_upload = client.post(
            "/api/signatures",
            headers=headers,
            files={"file": ("signature.png", image_bytes, "image/png")},
        )
        assert signature_upload.status_code == 200, signature_upload.text
        signature_url = signature_upload.json()["signature_url"]
        uploaded_files.append(Path(__file__).resolve().parents[1] / signature_url.lstrip("/"))
        signature_record = client.get("/api/signatures/me", headers=headers)
        assert signature_record.status_code == 200
        assert signature_record.json()["signature_url"] == signature_url
        assert client.get(signature_url).content == image_bytes

        stamp_upload = client.post(
            "/api/hr-stamp",
            headers=headers,
            files={"file": ("stamp.png", image_bytes, "image/png")},
        )
        assert stamp_upload.status_code == 200, stamp_upload.text
        stamp_url = stamp_upload.json()["stamp_url"]
        uploaded_files.append(Path(__file__).resolve().parents[1] / stamp_url.lstrip("/"))
        stamp_record = client.get("/api/hr-stamp", headers=headers)
        assert stamp_record.status_code == 200
        assert stamp_record.json()["stamp_url"] == stamp_url
        assert client.get(stamp_url).content == image_bytes
    finally:
        for uploaded_file in uploaded_files:
            uploaded_file.unlink(missing_ok=True)
        if user_id is not None:
            db.query(models.UserSignature).filter(models.UserSignature.user_id == user_id).delete()
            db.query(models.HRStamp).filter(models.HRStamp.uploaded_by == user_id).delete()
            db.query(models.User).filter(models.User.id == user_id).delete()
        db.commit()
        db.close()