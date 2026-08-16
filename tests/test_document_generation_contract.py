from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_document_generation_uses_direct_template_payload_contract():
    token_response = client.post(
        '/auth/token',
        data={'username': 'admin@peoplepluse.com', 'password': 'admin123'},
    )
    assert token_response.status_code == 200
    token = token_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    payload = {
        'template_type': 'appointment_letter',
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

    response = client.post('/documents/generate', json=payload, headers=headers)

    assert response.status_code == 200, response.text
    body = response.json()
    content = body.get('content', '')
    assert 'Jane Doe' in content
    assert 'jane@example.com' in content
    assert 'HR Officer' in content


def test_document_generate_docx_returns_word_file():
    token_response = client.post(
        '/auth/token',
        data={'username': 'admin@peoplepluse.com', 'password': 'admin123'},
    )
    assert token_response.status_code == 200
    token = token_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    payload = {
        'template_type': 'appointment_letter',
        'employee_name': 'Jane Doe',
        'employee_email': 'jane@example.com',
        'position': 'HR Officer',
        'department': 'People Operations',
        'start_date': '2026-01-01',
        'employment_type': 'Full-time',
        'manager_name': 'Jane Boss',
        'salary': '100000',
        'currency': 'KES',
        'benefits': 'Health insurance',
    }

    response = client.post('/documents/generate-docx', json=payload, headers=headers)
    assert response.status_code == 200, response.text
    assert response.headers['content-type'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    assert 'attachment' in response.headers['content-disposition']
    assert response.content[:2] == b'PK'


def test_document_generate_pdf_returns_pdf_file():
    token_response = client.post(
        '/auth/token',
        data={'username': 'admin@peoplepluse.com', 'password': 'admin123'},
    )
    assert token_response.status_code == 200
    token = token_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    payload = {
        'template_type': 'appointment_letter',
        'employee_name': 'Jane Doe',
        'employee_email': 'jane@example.com',
        'position': 'HR Officer',
        'department': 'People Operations',
        'start_date': '2026-01-01',
        'employment_type': 'Full-time',
        'manager_name': 'Jane Boss',
        'salary': '100000',
        'currency': 'KES',
        'benefits': 'Health insurance',
    }

    response = client.post('/documents/generate-pdf', json=payload, headers=headers)
    assert response.status_code == 200, response.text
    assert response.headers['content-type'] == 'application/pdf'
    assert response.content[:4] == b'%PDF'
