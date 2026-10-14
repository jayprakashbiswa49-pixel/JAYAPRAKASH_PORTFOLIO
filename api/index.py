import os
import sys

# Ensure root directory is on sys.path so the 'app' package is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

flask_app = create_app(os.environ.get("FLASK_ENV", "production"))


class VercelPathFix:
    """WSGI middleware to ensure PATH_INFO reflects the user's requested URL

    when Vercel rewrites incoming requests to /api/index.
    """

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # Vercel passes the original requested path in HTTP_X_MATCHED_PATH or HTTP_X_FORWARDED_URI
        matched_path = (
            environ.get("HTTP_X_MATCHED_PATH")
            or environ.get("HTTP_X_FORWARDED_URI")
            or environ.get("REQUEST_URI")
        )
        if matched_path:
            environ["PATH_INFO"] = matched_path.split("?")[0]
        elif environ.get("PATH_INFO", "").startswith("/api"):
            environ["PATH_INFO"] = "/"

        return self.wsgi_app(environ, start_response)


# Wrap with WSGI path fixer
flask_app.wsgi_app = VercelPathFix(flask_app.wsgi_app)

# Expose 'app' for Vercel's Python Serverless runtime
app = flask_app

if __name__ == "__main__":
    app.run()
