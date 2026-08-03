import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app
from backend.auth import create_access_token


def test_word_document_folder_upload_and_send_notification():
    client = TestClient(app)
    token = create_access_token({"sub": 1})

    response = client.post(
        "/api/documents/word-documents/bulk-upload",
        headers={"Authorization": f"Bearer {token}"},
        files=[
            ("files", ("sample_form.docx", b"test-word-bytes", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")),
        ],
    )

    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["success"] is True
    assert len(payload["uploaded"]) == 1

    send_response = client.post(
        "/api/documents/word-documents/send",
        headers={"Authorization": f"Bearer {token}"},
        json={"document_name": "sample_form.docx", "department": "finance"},
    )

    assert send_response.status_code == 200, send_response.text
    send_payload = send_response.json()
    assert send_payload["success"] is True
    assert send_payload["sent_to"]
