# Database Design & Persistence Strategy

**Document Status:** Approved Specification  
**Engines:** SQLite (Local Development) / PostgreSQL (Optional Render Production) / In-Memory Python Data Layer  

---

## 1. Data Classification & Persistence Rationale

A frequent antipattern in student and developer portfolio sites is putting static project cards and bio details into a database, introducing unnecessary runtime latency, migration complexity, and potential cold-start overhead on free-tier hosting (like Render).

In this architecture, data is categorized strictly into two tiers:

### Tier 1: Static / Portfolio Content (In-Memory Python Structures)
- **Entities**: Profile information, bio, social links, skill groups, project cards, education history, certifications.
- **Storage**: Structured Python module (`app/portfolio_data.py`).
- **Rationale**:
  - Zero latency (instant Jinja2 rendering in memory).
  - Version-controlled alongside codebase changes via Git.
  - Zero database dependency for core site viewing.
  - Impossible to attack via SQL injection on portfolio reads.

### Tier 2: Dynamic User Submissions (Optional Contact Persistence)
- **Entities**: Messages and inquiries submitted via `/contact`.
- **Storage**: Lightweight SQLAlchemy model (`ContactInquiry`) with SQLite default (`instance/portfolio.db`) and PostgreSQL support via `DATABASE_URL`.
- **Resilience**: The application features a **graceful degradation pattern**. If a database is not configured or fails to connect, the `EmailService` falls back to structured application logging so that no message is ever silently lost.

---

## 2. Schema Specification: `contact_inquiries`

When database persistence is enabled via `ENABLE_DB=True` or when `DATABASE_URL` is present in the environment, the following schema is utilized:

```sql
CREATE TABLE IF NOT EXISTS contact_inquiries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(80) NOT NULL,
    email VARCHAR(120) NOT NULL,
    subject VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ip_hash VARCHAR(64),
    status VARCHAR(20) DEFAULT 'new' NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_inquiries_submitted_at ON contact_inquiries (submitted_at DESC);
CREATE INDEX IF NOT EXISTS idx_inquiries_status ON contact_inquiries (status);
```

### Column Dictionary:
1. `id`: Primary key, auto-incrementing integer.
2. `name`: Sender's name, trimmed, sanitized, maximum 80 characters.
3. `email`: Sender's email address, RFC-compliant format, maximum 120 characters.
4. `subject`: Purpose of contact, maximum 150 characters.
5. `message`: In-depth inquiry body, sanitized text.
6. `submitted_at`: UTC timestamp of the submission.
7. `ip_hash`: SHA-256 hashed sender IP address (for rate-limiting / spam correlation without storing raw personal PII, adhering to privacy standards).
8. `status`: Lifecycle state (`new`, `read`, `replied`, `archived`).

---

## 3. SQLAlchemy Model Implementation (`app/models.py`)

```python
from datetime import datetime, timezone
from app import db

class ContactInquiry(db.Model):
    __tablename__ = 'contact_inquiries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    ip_hash = db.Column(db.String(64), nullable=True)
    status = db.Column(db.String(20), default='new', nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'submitted_at': self.submitted_at.isoformat(),
            'status': self.status
        }
```

---

## 4. Environment-Aware Connection Handling

- **Local / Default**:
  `sqlite:///{app.instance_path}/portfolio.db`
- **Render Production (PostgreSQL)**:
  `postgresql+psycopg2://user:password@host/dbname` (with automatic replacement of deprecated `postgres://` prefixes from Render environment variables to `postgresql://`).
- **Headless / Zero-DB Mode**:
  If `ENABLE_DB=False` is set in configuration, the app executes without initiating SQLAlchemy tables or database engines, storing submissions directly in structured log files (`logs/inquiries.log`).
