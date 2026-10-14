# Jayaprakash Biswal — Neumorphic Developer Portfolio

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.x-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Design](https://img.shields.io/badge/Design-Neumorphism%20Soft%20UI-4568DC.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Tests](https://img.shields.io/badge/Tests-15%20Passed%20(100%25)-success.svg)]()

A premium, responsive, professional developer portfolio built for **Jayaprakash Biswal**, an Information Technology Management student at **NIIS Group of Institutions, Bhubaneswar** (CGPA: 8.14). 

Engineered with a robust **Python & Flask** backend, **Jinja2 server-side rendering**, **Flask-WTF CSRF protection**, and a bespoke, accessible **Neumorphism design system** implemented in modern vanilla CSS3.

---

## 🌟 Highlights & Key Features

- **Soft Neumorphic Aesthetics**: Authentic physical dual-shadow simulation (`#C5C9CE` ambient shadow and `#FFFFFF` light specular highlight against an `#E8ECF1` canvas) with raised and inset surfaces.
- **Strict Accessibility (WCAG 2.1 AA)**: High contrast ratio (9.81:1 for primary headings and body copy, exceeding AAA standard), distinct keyboard focus indicators (`:focus-visible`), and `@media (prefers-reduced-motion)` support.
- **Flagship Project Showcases**:
  - **Glint: AI-Powered Placement Portal** (Python, Flask, SQLAlchemy, PostgreSQL) — [Live Demo](https://glint-placement-portal.onrender.com/) | [Repository](https://github.com/bishalraj-gouda/Glint)
  - **Customer Churn Prediction** (Python, Flask, Pandas, Scikit-learn) — [Repository](https://github.com/jayprakashbiswa49-pixel/Customer_Churn_Prediction)
- **Interactive Project Filtering**: Instant client-side categorization (Web & AI, Data Analytics & ML, Python Utilities) without layout jumps.
- **Secure Contact System**: Flask-WTF CSRF tokens, hidden anti-bot honeypot, RFC-compliant email validation, and dual-mode delivery (SMTP email dispatch with safe, structured fallback logging to `logs/inquiries.log`).
- **Production Ready**: Configured for Render deployment using multi-threaded **Gunicorn** WSGI workers and automated `/health` heartbeat monitoring.
- **100% Test Coverage**: Complete `pytest` test suite covering routes, resume delivery, error handlers, and form validations.

---

## 📁 Project Directory Layout

```text
INTERNSHIP_PORTFOLIO/
├── app/
│   ├── __init__.py               # Flask application factory (create_app), CSRF, security headers
│   ├── routes.py                 # Modular blueprint: /, /resume, /contact, /health
│   ├── forms.py                  # Flask-WTF ContactForm with CSRF, validation & honeypot
│   ├── portfolio_data.py         # Centralized developer profile, skills, projects & certs
│   ├── models.py                 # Optional SQLAlchemy ContactInquiry model
│   ├── services/
│   │   ├── __init__.py
│   │   └── email_service.py      # Resilient SMTP notification & file logging fallback
│   ├── templates/
│   │   ├── base.html             # Neumorphic master layout (navbar, mobile drawer, toasts, footer)
│   │   ├── index.html            # Main portfolio sections (hero, about, skills, projects, contact)
│   │   ├── 404.html              # Custom Neumorphic 404 page
│   │   └── 500.html              # Custom Neumorphic 500 page
│   └── static/
│       ├── css/
│       │   └── style.css         # Complete Neumorphic design system, tokens, responsive grid
│       ├── js/
│       │   └── main.js           # Smooth scroll, nav scroll spy, AJAX contact handler, drawer
│       ├── images/
│       │   ├── jb-monogram.svg   # Custom Neumorphic brand monogram
│       │   └── hero-illustration.svg # Custom Neumorphic Python & Data illustration
│       └── files/
│           └── resume.pdf        # Authentic PDF resume for Jayaprakash Biswal
├── docs/                         # Comprehensive engineering specifications
│   ├── PROJECT_OVERVIEW.md
│   ├── REQUIREMENTS.md
│   ├── UI_DESIGN_SYSTEM.md
│   ├── FLASK_ARCHITECTURE.md
│   ├── DATABASE_DESIGN.md
│   ├── IMPLEMENTATION_PLAN.md
│   ├── SECURITY_PLAN.md
│   ├── TESTING_PLAN.md
│   └── DEPLOYMENT_GUIDE.md
├── tests/                        # Automated pytest suite
│   ├── conftest.py
│   ├── test_routes.py
│   ├── test_forms.py
│   └── test_services.py
├── config.py                     # Environment configurations (Dev, Test, Prod)
├── requirements.txt              # Pinned production and test dependencies
├── .env.example                  # Environment configuration template
├── .gitignore                    # Version control exclusions
├── Procfile                      # Render WSGI process declaration
├── run.py                        # Local development runner
└── README.md                     # Documentation
```

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/jayprakashbiswa49-pixel/portfolio.git
cd portfolio

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy the example environment configuration:
```bash
cp .env.example .env
```
*(Optional)* Add your Gmail App Password if you want live SMTP email alerts upon contact form submissions. If omitted, inquiries are safely captured in `logs/inquiries.log`.

### 4. Run the Local Development Server
```bash
python run.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser to view the live portfolio.

---

## 🧪 Running Automated Tests

Run the complete test suite with verbose output:
```bash
pytest -v
```

All 15 test cases will execute:
- Route status checks (`/`, `/resume`, `/health`, 404 handler)
- Verification of authentic profile details, flagship projects, and credentials
- Form validation (required constraints, email validation, length boundaries)
- CSRF protection and anti-spam honeypot interception
- Service resilience and fallback logging

---

## ☁️ Deployment on Render

This portfolio is pre-configured for seamless, zero-downtime deployment on **Render**:

1. Push your repository to GitHub.
2. In the [Render Dashboard](https://dashboard.render.com), click **New +** &rarr; **Web Service**.
3. Connect your repository.
4. Set the following settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn "app:create_app()" -w 2 -b 0.0.0.0:$PORT`
5. Under **Environment Variables**, add:
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: `<generate-a-strong-secret-key>`
   - `CONTACT_RECIPIENT_EMAIL`: `jayprakashbiswa49@gmail.com`
6. Under **Advanced Settings**, set **Health Check Path** to `/health`.
7. Click **Deploy Web Service**.

For detailed setup, see [`docs/DEPLOYMENT_GUIDE.md`](docs/DEPLOYMENT_GUIDE.md).

---

## 👤 Developer Profile

- **Name**: Jayaprakash Biswal
- **Role**: Python Developer | Web Developer | Data Analyst | Aspiring Data Scientist
- **Education**: BSc in Information Technology Management (3rd Year, NIIS Group of Institutions, Bhubaneswar) — **CGPA: 8.14**
- **Email**: [jayprakashbiswa49@gmail.com](mailto:jayprakashbiswa49@gmail.com)
- **LinkedIn**: [https://www.linkedin.com/in/jayaprakash-biswal-bb1937414](https://www.linkedin.com/in/jayaprakash-biswal-bb1937414)
- **GitHub**: [https://github.com/jayprakashbiswa49-pixel](https://github.com/jayprakashbiswa49-pixel)

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
