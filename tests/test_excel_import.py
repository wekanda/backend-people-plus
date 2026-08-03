import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app
from backend.excel_import import _normalize_header, _map_row_data_to_employee_fields
from backend.auth import create_access_token


def test_normalize_header_supports_common_variants():
    assert _normalize_header("File Code") == "file_code"
    assert _normalize_header("Contact No.") == "contact_number"
    assert _normalize_header("Contract End") == "contract_end"


def test_map_row_data_to_employee_fields_handles_document_flags():
    row = {
        "application & resume": "missing",
        "appointment letter & job description": "present",
        "national id /driving permit": "missing",
    }

    mapped = _map_row_data_to_employee_fields(row)

    assert mapped["missing_app_resume"] is True
    assert mapped["missing_appointment_letter"] is False
    assert mapped["missing_national_id"] is True


def test_folder_import_route_is_exposed_for_hr_admin():
    client = TestClient(app)
    token = create_access_token({"sub": 1})

    response = client.post(
        "/api/excel/import-folder",
        headers={"Authorization": f"Bearer {token}"},
        json={},
    )

    assert response.status_code == 200
