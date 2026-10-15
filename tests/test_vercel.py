"""Tests for Vercel Serverless Function entrypoint and static asset routing."""
import os
import pytest
from werkzeug.test import Client
from werkzeug.wrappers import Response
from api.index import app


@pytest.fixture
def vercel_client():
    """Client configured for testing WSGI middleware in api/index.py."""
    return Client(app, Response)


def test_vercel_homepage_routing(vercel_client):
    """Test that homepage requested via Vercel rewrite returns 200 HTML."""
    response = vercel_client.get('/api/index?__path__=/')
    assert response.status_code == 200
    assert 'text/html' in response.content_type
    assert b'Jayaprakash Biswal' in response.data


def test_vercel_root_fallback(vercel_client):
    """Test fallback when Vercel invokes /api/index without query parameters."""
    response = vercel_client.get('/api/index')
    assert response.status_code == 200
    assert 'text/html' in response.content_type
    assert b'Jayaprakash Biswal' in response.data


def test_vercel_css_serving(vercel_client):
    """Test that static CSS requested via Vercel rewrite returns 200 and text/css."""
    response = vercel_client.get('/api/index?__path__=/static/css/style.css')
    assert response.status_code == 200
    assert 'text/css' in response.content_type
    assert b'--surface-base' in response.data or b'css' in response.data.lower()


def test_vercel_js_serving(vercel_client):
    """Test that static JS requested via Vercel rewrite returns 200 and JS MIME type."""
    response = vercel_client.get('/api/index?__path__=/static/js/main.js')
    assert response.status_code == 200
    assert 'javascript' in response.content_type


def test_vercel_svg_serving(vercel_client):
    """Test that static SVG images return 200 and image/svg+xml."""
    response = vercel_client.get('/api/index?__path__=/static/images/jb-monogram.svg')
    assert response.status_code == 200
    assert 'image/svg+xml' in response.content_type
    assert b'<svg' in response.data


def test_vercel_resume_serving(vercel_client):
    """Test that /resume requested via Vercel rewrite returns 200 and application/pdf."""
    response = vercel_client.get('/api/index?__path__=/resume')
    assert response.status_code == 200
    assert 'application/pdf' in response.content_type
    assert response.data.startswith(b'%PDF')


def test_public_static_directory_integrity():
    """Verify that public/static directory contains all required CDN assets."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    public_dir = os.path.join(project_root, 'public', 'static')

    required_assets = [
        os.path.join('css', 'style.css'),
        os.path.join('js', 'main.js'),
        os.path.join('images', 'jb-monogram.svg'),
        os.path.join('images', 'hero-illustration.svg'),
        os.path.join('files', 'resume.pdf')
    ]

    for asset in required_assets:
        full_path = os.path.join(public_dir, asset)
        assert os.path.isfile(full_path), f"Missing public CDN asset: {full_path}"
