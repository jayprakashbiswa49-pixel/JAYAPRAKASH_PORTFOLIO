import os
import logging
from datetime import datetime, timezone
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from config import config

# Global extension instances
csrf = CSRFProtect()
db = SQLAlchemy()


def create_app(config_name=None):
    """Application factory for the developer portfolio."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    # Allow passing a Config class directly (useful in test suites)
    if isinstance(config_name, type):
        selected_config = config_name
    else:
        selected_config = config.get(config_name, config['default'])

    app = Flask(__name__)
    app.config.from_object(selected_config)

    # Initialize extensions
    csrf.init_app(app)

    if app.config.get('ENABLE_DB', False):
        db.init_app(app)
        with app.app_context():
            # Ensure tables exist
            from app import models  # noqa: F401
            db.create_all()

    # Configure logging
    if not app.debug and not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Register global template context processors
    @app.context_processor
    def inject_global_data():
        return {
            'current_year': datetime.now(timezone.utc).year
        }

    # Security headers
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        # CSP allows Google Fonts for premium typography
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com data:; "
            "img-src 'self' data: https:; "
            "connect-src 'self';"
        )
        return response

    # Custom HTTP error boundaries
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error(f"Internal server error: {e}")
        return render_template('500.html'), 500

    @app.errorhandler(400)
    def bad_request(e):
        return render_template('404.html', error_title="400 - Bad Request",
                               error_message="The request could not be processed due to invalid parameters or missing CSRF tokens."), 400

    return app
