def test_index_route_success(client):
    """Verify that the home page renders with status 200 and authentic personal brand data."""
    response = client.get('/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    # Core personal brand assertions
    assert "Jayaprakash Biswal" in html
    assert "BSc in Information Technology Management" in html
    assert "NIIS Group of Institutions" in html
    assert "8.14" in html
    assert "Building useful digital experiences with Python, data, and AI." in html

    # Flagship project assertions
    assert "Glint: AI-Powered Placement Portal" in html
    assert "https://glint-placement-portal.onrender.com/" in html
    assert "https://github.com/bishalraj-gouda/Glint" in html
    assert "Customer Churn Prediction" in html
    assert "https://github.com/jayprakashbiswa49-pixel/Customer_Churn_Prediction" in html

    # Skills assertions
    assert "Python" in html
    assert "Flask" in html
    assert "Pandas" in html
    assert "Scikit-learn" in html

    # Certifications assertions
    assert "CodeWithHarry" in html
    assert "Job Ready Data Science" in html


def test_resume_route_inline(client):
    """Verify that GET /resume serves the valid PDF resume inline."""
    response = client.get('/resume')
    assert response.status_code == 200
    assert response.content_type == 'application/pdf'
    # Assert PDF magic bytes
    assert response.data.startswith(b'%PDF')


def test_resume_route_download_attachment(client):
    """Verify that GET /resume?download=1 delivers the PDF as an attachment."""
    response = client.get('/resume?download=1')
    assert response.status_code == 200
    assert response.content_type == 'application/pdf'
    content_disp = response.headers.get('Content-Disposition', '')
    assert 'attachment' in content_disp
    assert 'Jayaprakash_Biswal_Resume.pdf' in content_disp


def test_health_check_endpoint(client):
    """Verify that GET /health responds with 200 and monitoring metadata."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['app'] == 'Jayaprakash Biswal Portfolio'
    assert 'version' in data


def test_404_error_handling(client):
    """Verify that non-existent routes trigger the custom Neumorphic 404 handler."""
    response = client.get('/this-path-definitely-does-not-exist')
    assert response.status_code == 404
    html = response.get_data(as_text=True)
    assert "404" in html
    assert "Page Not Found" in html
    assert "Return to Portfolio" in html


def test_security_headers_present(client):
    """Verify that security headers are injected into HTTP responses."""
    response = client.get('/')
    assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    assert response.headers.get('X-Frame-Options') == 'SAMEORIGIN'
    assert response.headers.get('Referrer-Policy') == 'strict-origin-when-cross-origin'
    assert 'Content-Security-Policy' in response.headers
