import os
from app import create_app

# Instantiate the application for local running or serverless deployment (Vercel, Render, etc.)
env_name = os.environ.get("FLASK_ENV", "production")
app = create_app(env_name)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')
    print(f" * Starting Jayaprakash Biswal Portfolio server on http://127.0.0.1:{port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)
