import os
import sys

# Ensure root directory is on sys.path so the 'app' package is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

flask_app = create_app(os.environ.get("FLASK_ENV", "production"))


class VercelPathFix:
    """WSGI middleware ensuring Flask sees the original user URL path

    instead of internal rewrite targets.
    """

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # 1. Prefer actual requested URI if provided by Vercel's proxy
        raw_uri = (
            environ.get("REQUEST_URI")
            or environ.get("RAW_URI")
            or environ.get("HTTP_X_FORWARDED_URI")
        )
        if raw_uri:
            environ["PATH_INFO"] = raw_uri.split("?")[0]
        elif environ.get("PATH_INFO", "") in ("/api/index", "/api"):
            environ["PATH_INFO"] = "/"

        return self.wsgi_app(environ, start_response)


flask_app.wsgi_app = VercelPathFix(flask_app.wsgi_app)
app = flask_app

if __name__ == "__main__":
    app.run()
