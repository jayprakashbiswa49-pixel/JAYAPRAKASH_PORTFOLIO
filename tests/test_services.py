from app.services.email_service import EmailService
from app.portfolio_data import PROFILE_DATA, SKILL_GROUPS, PROJECTS, EDUCATION, CERTIFICATIONS


def test_email_service_fallback_without_smtp(app):
    """Verify that EmailService handles unconfigured SMTP safely without raising exceptions."""
    with app.app_context():
        # App config has no SMTP server in testing
        result = EmailService.send_inquiry(
            name="Test User",
            email="test@example.com",
            subject="Testing Fallback",
            message="This is a test message checking offline logging fallback.",
            ip_address="127.0.0.1"
        )
        assert result is True


def test_portfolio_data_integrity():
    """Verify that portfolio data contains valid links and structures."""
    assert PROFILE_DATA['name'] == 'Jayaprakash Biswal'
    assert PROFILE_DATA['email'] == 'jayprakashbiswa49@gmail.com'
    assert 'github.com' in PROFILE_DATA['github_url']
    assert 'linkedin.com' in PROFILE_DATA['linkedin_url']

    # Projects
    assert len(PROJECTS) >= 7
    glint = next(p for p in PROJECTS if p['id'] == 'glint')
    assert glint['featured'] is True
    assert glint['priority'] == 1
    assert 'onrender.com' in glint['live_demo_url']
    assert 'github.com' in glint['github_url']

    churn = next(p for p in PROJECTS if p['id'] == 'customer-churn')
    assert churn['featured'] is True
    assert churn['priority'] == 2

    # Skills
    assert len(SKILL_GROUPS) == 5
    categories = [g['category'] for g in SKILL_GROUPS]
    assert 'Programming Languages' in categories
    assert 'Web Development' in categories
    assert 'Data Analysis' in categories
    assert 'Machine Learning' in categories
    assert 'Tools & Workflow' in categories

    # Education & Certs
    assert EDUCATION['cgpa'] == '8.14'
    assert len(CERTIFICATIONS) == 5
