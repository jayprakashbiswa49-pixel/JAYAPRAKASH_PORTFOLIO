# Deployment Guide: Render & Production Environments

**Application:** Jayaprakash Biswal Developer Portfolio  
**Target Host:** [Render](https://render.com) (Web Service)  
**WSGI Server:** Gunicorn 21.x+  
**Python Runtime:** Python 3.10+  

---

## 1. Architecture for Production

In production, Flask's built-in development server (`app.run()`) must never be used. The application is served using **Gunicorn**, a production-grade WSGI HTTP Server, configured with multiple worker threads to handle concurrent visitors effortlessly.

```text
               Internet (Clients / Recruiters)
                             │
                             ▼
                    Render Cloud Edge / SSL
                             │ (Reverse Proxy)
                             ▼
            Gunicorn Master Process (Port $PORT)
            ├── Worker 1 (Thread 1..4)  --> Flask App Instance
            └── Worker 2 (Thread 1..4)  --> Flask App Instance
```

---

## 2. Deployment Artifacts

### A. Process File (`Procfile`)
Render automatically detects a `Procfile` at the root of the repository:
```text
web: gunicorn "app:create_app()" --workers 2 --threads 4 --timeout 60 --bind 0.0.0.0:$PORT
```

### B. Dependency Manifest (`requirements.txt`)
Contains all pinned production dependencies:
```text
Flask>=3.0.0
Flask-WTF>=1.2.0
WTForms>=3.1.0
email-validator>=2.1.0
Flask-SQLAlchemy>=3.1.0
python-dotenv>=1.0.0
gunicorn>=21.2.0
```

### C. Health Check Route
Render continuously monitors service vitality by querying:
`GET /health` -> HTTP 200 `{"status": "ok", "app": "Jayaprakash Biswal Portfolio"}`

---

## 3. Step-by-Step Render Deployment Workflow

### Step 1: Initialize Git & Push to GitHub
```bash
git init
git add .
git commit -m "feat: complete neumorphic flask developer portfolio"
git branch -M main
git remote add origin https://github.com/jayprakashbiswa49-pixel/portfolio.git
git push -u origin main
```

### Step 2: Create Web Service on Render
1. Log into your [Render Dashboard](https://dashboard.render.com).
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository (`portfolio`).
4. Configure the service properties:
   - **Name**: `jayaprakash-portfolio`
   - **Region**: Singapore or Frankfurt (choose nearest to target visitors)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn "app:create_app()" -w 2 -b 0.0.0.0:$PORT`
   - **Instance Type**: Free

### Step 3: Configure Environment Variables
Under the **Environment** tab on Render, add:

| Key | Example Value | Description |
| :--- | :--- | :--- |
| `FLASK_ENV` | `production` | Enables production safeguards |
| `SECRET_KEY` | `9f3c7b2e1a8d4c...` | Strong random hex string for CSRF signing |
| `CONTACT_RECIPIENT_EMAIL` | `jayprakashbiswa49@gmail.com` | Destination for contact form messages |
| `MAIL_SERVER` | `smtp.gmail.com` | *(Optional)* SMTP server for real-time alerts |
| `MAIL_PORT` | `587` | *(Optional)* SMTP port |
| `MAIL_USE_TLS` | `True` | *(Optional)* TLS encryption toggle |
| `MAIL_USERNAME` | `jayprakashbiswa49@gmail.com` | *(Optional)* Gmail address |
| `MAIL_PASSWORD` | `xxxx-xxxx-xxxx-xxxx` | *(Optional)* Gmail 16-character App Password |

> **Note**: If SMTP credentials are not configured, inquiries are still captured safely and logged to the persistent application log.

### Step 4: Configure Health Check Path
Under **Advanced Settings**:
- Set **Health Check Path** to `/health`.
Render will now perform zero-downtime deploys and auto-restart if the service ever becomes unresponsive.

---

## 4. Local Run & Verification

Before deploying, test locally with Gunicorn or the development runner:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run local development server
python run.py
# Server runs at http://127.0.0.1:5000/

# 3. Test local production Gunicorn emulation (on Unix/WSL/Docker)
gunicorn "app:create_app()" -w 2 -b 127.0.0.1:5000
```
