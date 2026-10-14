from app import create_app
from config import Config


def test_valid_contact_submission_ajax(client):
    """Test successful AJAX contact inquiry submission."""
    payload = {
        'name': 'Sarah Connor',
        'email': 'sarah@example.com',
        'subject': 'Software Internship Opportunity',
        'message': 'Hello Jayaprakash, we reviewed your Glint project and would like to speak with you regarding an internship role.',
        'hp_website': ''
    }
    response = client.post('/contact', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert "Thank you" in data['message']


def test_valid_contact_submission_form_encoded(client):
    """Test successful standard HTML form-encoded POST submission."""
    form_data = {
        'name': 'David Miller',
        'email': 'david.miller@example.org',
        'subject': 'Collaboration on Data Analytics',
        'message': 'Interested in collaborating on your sales analysis and machine learning workflows.',
        'hp_website': ''
    }
    response = client.post('/contact', data=form_data, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/#contact') or '/#contact' in response.headers['Location']


def test_missing_required_fields_ajax(client):
    """Test that missing required fields trigger validation errors."""
    payload = {
        'name': '',
        'email': 'valid@example.com',
        'subject': '',
        'message': 'Short'
    }
    response = client.post('/contact', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert 'name' in data['errors']
    assert 'subject' in data['errors']
    assert 'message' in data['errors']


def test_invalid_email_syntax_ajax(client):
    """Test that malformed email addresses are rejected."""
    payload = {
        'name': 'John Doe',
        'email': 'not-a-valid-email-string',
        'subject': 'General Inquiry',
        'message': 'This is a sufficiently long message for testing email validation.'
    }
    response = client.post('/contact', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert 'email' in data['errors']


def test_message_length_boundary(client):
    """Test that messages under 10 characters are rejected."""
    payload = {
        'name': 'Jane Doe',
        'email': 'jane@example.com',
        'subject': 'Hello',
        'message': 'Too short'  # 9 chars
    }
    response = client.post('/contact', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'message' in data['errors']


def test_honeypot_spam_interception_ajax(client):
    """Test that bot submissions with the honeypot field filled are silently discarded."""
    payload = {
        'name': 'Spam Bot',
        'email': 'bot@spammer.net',
        'subject': 'Buy crypto now',
        'message': 'We have special offers for you click here immediately.',
        'hp_website': 'http://malicious-spam-site.com'
    }
    response = client.post('/contact', json=payload)
    # Returns 200 to not alert spam crawler
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_csrf_protection_enforced_when_enabled():
    """Verify that requests without CSRF token are blocked when WTF_CSRF_ENABLED is True."""
    class CsrfTestConfig(Config):
        TESTING = True
        WTF_CSRF_ENABLED = True
        SECRET_KEY = 'test-csrf-enforcement-key'

    csrf_app = create_app(CsrfTestConfig)
    csrf_client = csrf_app.test_client()

    # Post without CSRF token
    response = csrf_client.post('/contact', data={
        'name': 'Hacker',
        'email': 'hacker@example.com',
        'subject': 'CSRF Attack Attempt',
        'message': 'Testing whether CSRF validation intercepts this request.'
    })
    # Flask-WTF rejects with 400 Bad Request
    assert response.status_code == 400
