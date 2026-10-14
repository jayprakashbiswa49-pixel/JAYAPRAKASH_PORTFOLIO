# Requirements Specification: Neumorphic Flask Developer Portfolio

**Document Status:** Approved Draft  
**Target Platform:** Python 3.10+ / Flask / Render / Gunicorn / Modern Web Browsers  

---

## 1. Functional Requirements (FR)

### FR-01: Navigation & Layout
- **FR-01.1**: The application shall present a fixed/sticky Neumorphic top navigation bar displaying:
  - Personal Brand Wordmark ("JB" monogram + "Jayaprakash Biswal")
  - Anchor links to sections: Home, About, Skills, Projects, Education, Contact
  - Quick action: "Resume" download / preview button
  - Theme/Visual indicator and accessible mobile toggle (hamburger menu)
- **FR-01.2**: Navigation must smoothly scroll to corresponding target sections using native smooth-scrolling with scroll-margin offset to account for navbar height.
- **FR-01.3**: The mobile navigation drawer must open and close smoothly with accessible ARIA state (`aria-expanded`, `aria-controls`), trapping focus when opened and closing upon link selection or backdrop click.

### FR-02: Hero Presentation
- **FR-02.1**: Prominently display the primary headline: *"Building useful digital experiences with Python, data, and AI."*
- **FR-02.2**: Present the official introduction: *"I'm Jayaprakash Biswal, an IT Management student passionate about Python development, data analysis, and practical AI-powered applications."*
- **FR-02.3**: Render primary call-to-actions:
  - "Explore Projects" (links to `#projects`)
  - "Contact Me" (links to `#contact`)
  - "Download Resume" (triggers `/resume`)
- **FR-02.4**: Provide direct, verifiable links to GitHub (`https://github.com/jayprakashbiswa49-pixel`) and LinkedIn (`https://www.linkedin.com/in/jayaprakash-biswal-bb1937414`).
- **FR-02.5**: Render a custom Neumorphic illustration (layered geometric/data composition or code matrix) without stock/fake human photos.

### FR-03: About Me
- **FR-03.1**: Present academic journey at NIIS Group of Institutions, Bhubaneswar (BSc in Information Technology Management, 3rd Year, CGPA: 8.14).
- **FR-03.2**: Detail professional interests: Python backends, Exploratory Data Analysis (EDA), predictive modeling, and building utility software.
- **FR-03.3**: Provide key metric highlights (e.g., 7+ Featured Projects, 5 Certifications, 8.14 CGPA) rendered in distinct Neumorphic tiles.

### FR-04: Technical Skills Showcase
- **FR-04.1**: Group skills into 5 logical categories:
  1. *Programming*: Python, Java, C, SQL, JavaScript
  2. *Web Development*: HTML5, CSS3, Flask, Jinja2, REST APIs
  3. *Data Analysis*: Pandas, NumPy, Matplotlib, Seaborn, Excel, Power BI
  4. *Machine Learning*: Scikit-learn, Data Preprocessing, Machine Learning Fundamentals
  5. *Tools & Workflow*: Git, GitHub, VS Code, Jupyter Notebook, Anaconda
- **FR-04.2**: Avoid arbitrary percentage indicators or deceptive level ratings; display clean Neumorphic chips with category badges and contextual tooltips.

### FR-05: Featured Projects
- **FR-05.1**: Highlight **Glint: AI-Powered Placement Portal** as Tier-1 Flagship (with Live Demo link to `https://glint-placement-portal.onrender.com/` and GitHub repo `https://github.com/bishalraj-gouda/Glint`).
- **FR-05.2**: Highlight **Customer Churn Prediction** as Tier-1 Machine Learning showcase (with GitHub repo `https://github.com/jayprakashbiswa49-pixel/Customer_Churn_Prediction`).
- **FR-05.3**: Display remaining verified projects in a responsive Neumorphic grid:
  - *Sales Data Analysis* (Python, Pandas, Matplotlib)
  - *Amazon Books Analysis* (Python, Pandas, Data Visualization)
  - *IPL Data Analysis* (Python, Pandas, Matplotlib)
  - *Modern UI* (HTML5, CSS3)
  - *Python Hands-on Projects* (Python, APIs, PyPDF2)
- **FR-05.4**: Each project card must display title, category pill, concise feature description, technology tags, and direct repository / live demo links.
- **FR-05.5**: Allow interactive filtering by category: All, Web & Full-Stack, Data Analytics & ML, Python Utilities.

### FR-06: Education & Certifications
- **FR-06.1**: Education timeline card for BSc in IT Management at NIIS Group of Institutions, Bhubaneswar.
- **FR-06.2**: Credentials grid showing 5 verified certifications:
  - Job Ready Data Science (CodeWithHarry)
  - Python Bootcamp (CodeWithHarry)
  - AI Excel (SkillCourse)
  - Power BI (Great Learning / SkillCourse)
  - Web Development (Apna College)
- **FR-06.3**: Display issuing organization without fabricated credential IDs or expired verification links.

### FR-07: Contact System
- **FR-07.1**: Provide a secure contact form with inputs for:
  - Name (min 2, max 80 chars)
  - Email (valid RFC-compliant email, max 120 chars)
  - Subject (min 3, max 150 chars)
  - Message (min 10, max 2000 chars)
- **FR-07.2**: Implement Flask-WTF with CSRF token generation and server-side validation.
- **FR-07.3**: Include client-side instant validation with accessible feedback messages.
- **FR-07.4**: Support dual submission modes:
  - Progressive enhancement via asynchronous `fetch` (JSON response) with smooth in-place toast notifications.
  - Standard HTML form POST fallback for clients with JavaScript disabled.
- **FR-07.5**: Integrate email dispatch via Python `smtplib`/Flask-Mail support through environment variables (`MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_USE_TLS`). Provide automatic fallback to persistent SQLite logging and application logger if SMTP credentials are not set.
- **FR-07.6**: Integrate anti-spam honeypot input field (`hp_website`, hidden via CSS and off-screen positioning; rejecting any submission where this field is filled).

### FR-08: Resume Serving & Health Check
- **FR-08.1**: Route `GET /resume` must safely send Jayaprakash Biswal's actual PDF resume from static storage with appropriate MIME headers (`application/pdf`) and inline/attachment options.
- **FR-08.2**: Route `GET /health` must return `200 OK` with JSON payload containing system status, timestamp, and environment mode for Render deployment monitors.
- **FR-08.3**: Implement custom error handlers for `404 Not Found` and `500 Internal Server Error` styled with the Neumorphic design system.

---

## 2. Non-Functional Requirements (NFR)

### NFR-01: Performance & Efficiency
- Time-to-First-Byte (TTFB) < 150ms on warm Gunicorn worker.
- Total uncompressed static CSS < 40KB; Vanilla JS < 25KB (zero heavy third-party UI libraries like jQuery, Bootstrap, or React).
- All image assets optimized (SVG vector assets or compressed modern WebP).

### NFR-02: Accessibility (a11y) & Usability
- Full compliance with WCAG 2.1 Level AA standards.
- Primary text (`#202936`) on base background (`#E8ECF1`) yields **9.8:1** contrast ratio (exceeds AAA standard of 7:1).
- Secondary muted text (`#657080`) yields **4.55:1** contrast ratio (meets AA standard).
- Distinct keyboard `:focus-visible` styling with `2px solid #4568DC` and `2px offset`.
- Interactive components have minimum touch targets of `44px x 44px`.
- Media query `@media (prefers-reduced-motion: reduce)` disables or dampens transitions.

### NFR-03: Security & Data Integrity
- Robust protection against Cross-Site Request Forgery (CSRF) via Flask-WTF secret salts.
- Input sanitization and HTML escaping in Jinja2 templates (prevents XSS).
- Secure HTTP response headers (Content-Security-Policy, X-Content-Type-Options: nosniff, X-Frame-Options: SAMEORIGIN, Referrer-Policy: strict-origin-when-cross-origin).
- No hardcoded API keys or passwords in version control.

### NFR-04: Cross-Device Responsiveness
- Seamless rendering across viewports:
  - Mobile (320px – 640px)
  - Tablet (641px – 1024px)
  - Laptop / Desktop (1025px – 1440px)
  - Ultra-wide (> 1440px, centered with max-width container of 1200px)
- Zero horizontal scrolling under any viewport resolution.

### NFR-05: Maintainability & Extensibility
- Centralized data dictionary in `app/portfolio_data.py`. Updating a project, certification, or skill requires editing a single Python data structure without touching template markup.
- Clear directory separation adhering to Flask Application Factory best practices.
