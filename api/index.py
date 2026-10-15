import os
import sys
import urllib.parse

# Ensure root directory is on sys.path so the 'app' package is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

flask_app = create_app(os.environ.get("FLASK_ENV", "production"))


class VercelPathFix:
    """WSGI middleware ensuring Flask sees the original user URL path
    instead of internal rewrite targets on Vercel.
    """

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # 1. Extract original requested path if passed via __path__ in vercel.json rewrite
        qs = environ.get("QUERY_STRING", "")
        if "__path__" in qs:
            params = urllib.parse.parse_qs(qs, keep_blank_values=True)
            if "__path__" in params:
                path = params.pop("__path__")[0]
                while path.startswith("//"):
                    path = path[1:]
                environ["PATH_INFO"] = path if path.startswith("/") else "/" + path
                # Rebuild remaining query string without internal __path__ param
                environ["QUERY_STRING"] = urllib.parse.urlencode(
                    [(k, v) for k, vs in params.items() for v in vs]
                )
        # 2. Prefer actual requested URI if provided by proxy headers
        elif environ.get("HTTP_X_FORWARDED_URI"):
            environ["PATH_INFO"] = environ["HTTP_X_FORWARDED_URI"].split("?")[0]
        elif environ.get("REQUEST_URI"):
            environ["PATH_INFO"] = environ["REQUEST_URI"].split("?")[0]
        elif environ.get("RAW_URI"):
            environ["PATH_INFO"] = environ["RAW_URI"].split("?")[0]
        elif environ.get("PATH_INFO", "") in ("/api/index", "/api", "/api/index.py"):
            environ["PATH_INFO"] = "/"

        return self.wsgi_app(environ, start_response)


flask_app.wsgi_app = VercelPathFix(flask_app.wsgi_app)
app = flask_app

if __name__ == "__main__":
    app.run()
