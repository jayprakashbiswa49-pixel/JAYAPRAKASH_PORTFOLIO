import pytest
from app import create_app
from config import TestingConfig


@pytest.fixture
def app():
    """Create and configure a clean testing instance of the Flask application."""
    app = create_app(TestingConfig)
    yield app


@pytest.fixture
def client(app):
    """Test client for simulating HTTP requests without running a live server."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI runner fixture for Flask command line operations."""
    return app.test_cli_runner()
