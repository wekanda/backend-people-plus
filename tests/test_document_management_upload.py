from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_document_upload_route_accepts_current_contract_and_employee_documents_have_status_shape():
    token_response = client.post(
        '/auth/token',
        data={'username': 'admin@peoplepluse.com', 'password': 'admin123'},
    )
    assert token_response.status_code == 200
    token = token_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    upload_response = client.post(
        '/api/documents/upload?employee_id=1&document_type_id=1',
        files={'file': ('test.txt', b'hello world', 'text/plain')},
        headers=headers,
    )
    assert upload_response.status_code == 200, upload_response.text

    documents_response = client.get('/api/documents/employee/1', headers=headers)
    assert documents_response.status_code == 200, documents_response.text
    payload = documents_response.json()
    assert isinstance(payload, list)
    assert any('approval_status' in doc for doc in payload)
