from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_document_send_uses_direct_template_payload_contract():
    token_response = client.post(
        '/auth/token',
        data={'username': 'admin@peoplepluse.com', 'password': 'admin123'},
    )
    assert token_response.status_code == 200
    token = token_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    payload = {
        'template_type': 'appointment_letter',
        'email': 'recipient@example.com',
        'employee_name': 'Jane Doe',
        'employee_email': 'jane@example.com',
        'employee_address': 'Nairobi',
        'position': 'HR Officer',
        'department': 'People Operations',
        'start_date': '2026-01-01',
        'employment_type': 'Full-time',
        'manager_name': 'Jane Boss',
        'salary': '100000',
        'currency': 'KES',
        'benefits': 'Health insurance',
    }

    response = client.post('/documents/send', json=payload, headers=headers)

    assert response.status_code == 200, response.text
    body = response.json()
    assert 'ready to send' in body.get('message', '')
    assert 'saved_path' in body
