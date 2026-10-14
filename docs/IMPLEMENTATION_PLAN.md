# Step-by-Step Implementation Plan

**Portfolio for:** Jayaprakash Biswal  
**Target Architecture:** Flask 3.x + Neumorphic UI Design System + Render WSGI  

---

## Phase 1: Environment & Directory Scaffolding
- [x] Inspect project directory and establish structure.
- [x] Create comprehensive architecture and design specification documentation in `docs/`.
- [ ] Initialize Python virtual environment configuration and `requirements.txt`:
  - `Flask>=3.0.0`
  - `Flask-WTF>=1.2.0`
  - `WTForms>=3.1.0`
  - `email-validator>=2.1.0`
  - `Flask-SQLAlchemy>=3.1.0`
  - `python-dotenv>=1.0.0`
  - `gunicorn>=21.2.0`
  - `pytest>=8.0.0`
  - `pytest-flask>=1.3.0`
- [ ] Create `.env.example` and `.gitignore` (ignoring `.env`, `instance/`, `__pycache__`, `.pytest_cache`, virtual environments).

---

## Phase 2: Configuration & Centralized Data Layer
- [ ] Implement `config.py` with `Config`, `DevelopmentConfig`, `TestingConfig`, and `ProductionConfig`.
- [ ] Build `app/portfolio_data.py`:
  - Personal branding details (Jayaprakash Biswal, location, education, CGPA: 8.14, email, LinkedIn, GitHub).
  - 5 Categorized skill groups without arbitrary percentages.
  - 7 Verified project entries with Glint and Customer Churn Prediction prioritized as flagships.
  - 5 Verified certifications.
  - Academic background at NIIS Group of Institutions.

---

## Phase 3: Backend Core, Forms & Services
- [ ] Implement `app/forms.py`:
  - `ContactForm` using Flask-WTF with CSRF token.
  - StringField `name`, EmailField `email`, StringField `subject`, TextAreaField `message`.
  - Anti-spam hidden honeypot field `hp_website`.
- [ ] Implement `app/services/email_service.py`:
  - Dual-mode notification service.
  - SMTP dispatch if environment variables (`MAIL_SERVER`, etc.) are configured.
  - Fallback structured logging (`logs/inquiries.log` & console) to prevent failures when offline.
- [ ] Implement `app/models.py` for optional SQLite/PostgreSQL inquiry tracking.
- [ ] Implement `app/__init__.py` using Application Factory (`create_app`), registering CSRF protection and database extensions.
- [ ] Implement `app/routes.py`:
  - `GET /` : Render portfolio with Jinja2 context.
  - `GET /resume` : Serve actual `resume.pdf` with proper MIME headers.
  - `POST /contact` : Dual AJAX/JSON and standard form POST handler.
  - `GET /health` : JSON health status.
  - Error handlers: 404 and 500 pages.

---

## Phase 4: Neumorphic Frontend & Jinja2 Templates
- [ ] Build `app/static/css/style.css`:
  - Root tokens (`--bg: #E8ECF1`, `--text: #202936`, `--accent: #4568DC`, `--shadow-raised`, `--shadow-inset`).
  - Strict typography rules, focus rings, and high contrast styling.
  - Neumorphic cards, buttons, navbars, badges, and form controls.
  - Fluid responsive grid (mobile, tablet, desktop) with no horizontal overflow.
  - Reduced-motion accessibility media query.
- [ ] Create static visual assets:
  - `app/static/images/jb-monogram.svg`: Elegant brand mark.
  - `app/static/images/hero-illustration.svg`: Custom tactile Neumorphic abstract composition representing data and Python.
  - `app/static/files/resume.pdf`: Professional resume document.
- [ ] Build Jinja2 templates:
  - `app/templates/base.html`: Document shell, meta tags, Neumorphic navbar, toast container, footer.
  - `app/templates/index.html`: Hero, About, Skills, Projects (with interactive filters), Education, Certifications, Contact sections.
  - `app/templates/404.html`: Neumorphic 404 page with return-home button.
  - `app/templates/500.html`: Neumorphic 500 page.
- [ ] Build `app/static/js/main.js`:
  - Accessible mobile drawer toggle with ARIA synchronization.
  - Smooth scroll with fixed-header offset.
  - Active navigation scroll spy via `IntersectionObserver`.
  - Interactive project category filtering.
  - AJAX contact form submission with instant feedback toasts and fallback to standard POST.

---

## Phase 5: Automated Testing & Validation
- [ ] Configure `tests/conftest.py` with Flask test client fixtures.
- [ ] Implement `tests/test_routes.py`:
  - Validate `GET /` returns 200 and contains personal brand identifiers.
  - Validate `GET /resume` serves PDF with 200.
  - Validate `GET /health` returns 200 and expected JSON payload.
  - Validate 404 error page.
- [ ] Implement `tests/test_forms.py`:
  - Test valid form submission returns success.
  - Test missing required fields return validation errors.
  - Test invalid email formats return validation errors.
  - Test honeypot trigger rejects spam submissions.
  - Test CSRF protection blocks forged submissions.
- [ ] Execute `pytest` and verify 100% test pass rate.

---

## Phase 6: Production Readiness & Quality Assurance
- [ ] Prepare `run.py` and `Procfile` (`web: gunicorn "app:create_app()" -w 2 -b 0.0.0.0:$PORT`).
- [ ] Validate cross-viewport responsive design and accessibility standards.
- [ ] Write comprehensive `README.md` with local setup and Render deployment instructions.
