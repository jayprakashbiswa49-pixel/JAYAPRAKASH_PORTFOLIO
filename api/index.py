import os
import sys

# Ensure root directory is on sys.path so the 'app' package is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

# Instantiate Flask application for Vercel Serverless Function
app = create_app(os.environ.get("FLASK_ENV", "production"))

if __name__ == "__main__":
    app.run()
