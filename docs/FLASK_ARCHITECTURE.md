# Flask Architecture & Backend Specification

**Pattern:** Application Factory Pattern with Modular Blueprints  
**Language:** Python 3.10+  
**Framework:** Flask 3.x with Jinja2, Flask-WTF, Werkzeug  

---

## 1. Architectural Overview

The backend is engineered according to Python enterprise best practices, employing the **Application Factory pattern** (`create_app`). This guarantees:
1. **Isolated Testing**: Tests can instantiate clean application contexts with in-memory configurations without polluting state.
2. **Environment Segregation**: Distinct configurations for Development, Testing, and Render Production.
3. **Decoupled Data Layer**: Personal portfolio details, projects, skills, and certifications reside in `app/portfolio_data.py` as typed data structures, eliminating brittle database queries for immutable portfolio data while retaining full Pythonic extensibility.
4. **Service Abstraction**: Side effects like email notifications and contact logging are delegated to `app/services/email_service.py` with automatic fallbacks so that misconfigured SMTP will never crash user inquiries.

---

## 2. Codebase Directory Structure

```text
INTERNSHIP_PORTFOLIO/
├── app/
│   ├── __init__.py               # Application factory (create_app), extension initialization
│   ├── routes.py                 # Core Blueprint: /, /resume, /contact, /health
│   ├── forms.py                  # Flask-WTF ContactForm with CSRF & Honeypot
│   ├── portfolio_data.py         # Centralized profile, skills, projects, certifications dictionary
│   ├── models.py                 # Optional SQLAlchemy ContactInquiry model for persistent persistence
│   ├── services/
│   │   ├── __init__.py
│   │   └── email_service.py      # Resilient SMTP notification & fallback console/file logger
│   ├── templates/
│   │   ├── base.html             # Neumorphic master template (meta, CSS tokens, header, footer)
│   │   ├── index.html            # Main portfolio page with modular sections
│   │   ├── 404.html              # Custom Neumorphic 404 page
│   │   └── 500.html              # Custom Neumorphic 500 error page
│   └── static/
│       ├── css/
│       │   └── style.css         # Complete Neumorphic design system, components, responsive layout
│       ├── js/
│       │   └── main.js           # Smooth scroll, active nav spy, AJAX contact handler, mobile drawer
│       ├── images/
│       │   ├── jb-monogram.svg   # Custom SVG monogram
│       │   └── hero-illustration.svg # Tactile Neumorphic geometric data composition
│       └── files/
│           └── resume.pdf        # Jayaprakash Biswal's actual PDF resume
├── docs/                         # Architecture, security, design, and deployment specifications
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures (client, app, test_config)
│   ├── test_routes.py            # Endpoints tests (/, /resume, /health, error pages)
│   └── test_forms.py             # Form validation, CSRF, honeypot, and submission handling
├── config.py                     # Config classes: DevelopmentConfig, TestingConfig, ProductionConfig
├── requirements.txt              # Pinned production and test dependencies
├── .env.example                  # Template for required environment variables
├── .gitignore                    # Python, virtualenv, IDE, cache, and secrets exclusion
├── run.py                        # Local execution entrypoint
├── Procfile                      # Render / Heroku process declaration (Gunicorn)
└── README.md                     # Complete project documentation and quickstart
```

---

## 3. Endpoints & Route Definitions

| Method | Endpoint | Handler | Description | Request Payload | Response |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | `routes.index` | Renders main portfolio | None | HTML (`index.html`) with injected portfolio data & empty CSRF-protected `ContactForm` |
| `GET` | `/resume` | `routes.download_resume` | Serves official resume | Query param `?download=1` (optional) | `application/pdf` (inline display or attachment) |
| `POST` | `/contact` | `routes.submit_contact` | Validates & logs contact inquiry | Form-encoded or JSON: `{name, email, subject, message, hp_website, csrf_token}` | JSON: `{"success": true, "message": "..."}` or redirect with flash |
| `GET` | `/health` | `routes.health_check` | Production readiness check | None | JSON: `{"status": "ok", "app": "Jayaprakash Biswal Portfolio", "version": "1.0.0"}` |
| `404` | Error Handler | `routes.handle_404` | Custom Not Found page | None | HTML (`404.html`) with status code `404` |
| `500` | Error Handler | `routes.handle_500` | Custom Server Error page | None | HTML (`500.html`) with status code `500` |

---

## 4. Centralized Data Architecture (`portfolio_data.py`)

All personal information, project summaries, category tags, repository links, skill taxonomy, and academic credentials are maintained within typed, read-only dictionaries in `portfolio_data.py`.

### Structure:
- `PROFILE_DATA`: Full name, moniker, tagline, bio, contact email, social links, location, education overview.
- `SKILL_GROUPS`: Organized into 5 distinct categories with icon descriptors.
- `PROJECTS`: List of structured project objects:
  ```python
  {
      "id": "glint",
      "title": "Glint: AI-Powered Placement Portal",
      "featured": True,
      "priority": 1,
      "category": "Web & AI",
      "description": "An AI-oriented placement platform designed to support student profiles, skill-gap identification, candidate matching, and placement workflows.",
      "tech_stack": ["Python", "Flask", "SQLAlchemy", "PostgreSQL"],
      "github_url": "https://github.com/bishalraj-gouda/Glint",
      "live_demo_url": "https://glint-placement-portal.onrender.com/",
      "badge": "Flagship Project"
  }
  ```
- `CERTIFICATIONS`: List of authentic certifications with issuing institutions.
- `EDUCATION`: Degree, institution, year, CGPA, coursework details.

---

## 5. Contact Processing & Email Service Subsystem

```text
[User Contact Form Submission]
              │
              ▼
   [Honeypot Check (hp_website)]
   ├── If filled: Log bot attempt, return 200 (silent discard)
   └── If clean: Proceed
              │
              ▼
   [Flask-WTF Validation]
   ├── Name length, RFC email check, message length
   ├── CSRF token verification
   └── If invalid: Return 400 with field errors
              │
              ▼
   [EmailService.send_inquiry()]
   ├── Check environment variables (MAIL_SERVER, MAIL_USERNAME, etc.)
   ├── If SMTP available: Send notification email to jayprakashbiswa49@gmail.com
   └── If SMTP absent: Fallback gracefully to structured file/console logging
              │
              ▼
   [Optional DB Persistence]
   └── If SQLAlchemy enabled: Record inquiry into SQLite/PostgreSQL
              │
              ▼
   [Response Delivery]
   ├── AJAX: JSON {success: true, message: "Thank you..."}
   └── HTML Form: Flash message + redirect to /#contact
```

---

## 6. Template Hierarchy & Jinja2 Macros

- `base.html`:
  - Defines the global document head (meta viewport, OpenGraph tags, semantic title, CSS styles).
  - Renders the sticky Neumorphic navbar and accessible mobile drawer.
  - Houses the flash messages container (rendered as Neumorphic floating toasts).
  - Renders the Neumorphic footer and back-to-top button.
  - Injects CSRF token in `<meta name="csrf-token" content="...">` for JavaScript fetch calls.
- `index.html`:
  - Extends `base.html`.
  - Sections: Hero (`#hero`), About (`#about`), Skills (`#skills`), Projects (`#projects`), Education & Certifications (`#education`), Contact (`#contact`).
- Macros:
  - `render_project_card(project)`: Renders project with raised card styling, tag pills, and verified links.
  - `render_skill_group(group)`: Renders grouped skills with soft chip styling.
