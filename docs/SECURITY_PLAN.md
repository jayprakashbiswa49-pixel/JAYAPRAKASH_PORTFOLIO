# Security Plan & Hardening Strategy

**Target Application:** Jayaprakash Biswal Developer Portfolio (Flask 3.x)  
**Security Standard:** OWASP Top 10 Aligned  

---

## 1. Threat Modeling & Attack Surface

| Asset / Endpoint | Threat Vector | Mitigation Strategy |
| :--- | :--- | :--- |
| `POST /contact` | Cross-Site Request Forgery (CSRF) | Flask-WTF cryptographic CSRF tokens, checked on every state-changing request |
| `POST /contact` | Spam bots / Automated form flood | Hidden honeypot field (`hp_website`), client & server-side length limits |
| `POST /contact` | Cross-Site Scripting (XSS) | Jinja2 auto-escaping on all renders, strict WTForms input sanitization |
| `GET /resume` | Path Traversal / Arbitrary File Read | Flask `send_from_directory` scoped strictly to `app/static/files` |
| Application Wide | Clickjacking & MIME Sniffing | HTTP Security headers: `X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff` |
| Application Wide | Information Disclosure | `DEBUG=False` in production; custom 404/500 handlers concealing stack traces |
| Configuration | Credential Leakage | Zero secrets stored in Git; loaded via `.env` / environment variables |

---

## 2. CSRF Architecture & Token Handling

Flask-WTF provides robust CSRF protection initialized globally via `CSRFProtect(app)`.

### A. Server-Side Token Generation
Every contact form renders a hidden CSRF token generated per session:
```html
<form method="POST" action="{{ url_for('routes.submit_contact') }}">
  {{ form.csrf_token }}
  <!-- Input fields -->
</form>
```

### B. Asynchronous (AJAX) Fetch CSRF Transmission
In `base.html`, the CSRF token is exposed via a secure meta tag:
```html
<meta name="csrf-token" content="{{ csrf_token() }}">
```
In `main.js`, fetch requests automatically extract this token and append it to the request header:
```javascript
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
fetch('/contact', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrfToken
  },
  body: JSON.stringify(formData)
});
```

---

## 3. Anti-Bot Honeypot Defense

Automated spam crawlers fill all discovered inputs in a `<form>`. We introduce a honeypot field that is invisible to human users but tempting to bots:
```html
<div class="hp-wrapper" aria-hidden="true" tabindex="-1">
  <label for="hp_website">Leave this field blank</label>
  <input type="text" id="hp_website" name="hp_website" autocomplete="off">
</div>
```
```css
.hp-wrapper {
  position: absolute !important;
  left: -9999px !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
```

In `routes.py`:
```python
if form.hp_website.data:
    # Silent discard to avoid tipping off bot operators
    logger.warning("Spam honeypot triggered from IP: %s", get_client_ip())
    return jsonify({"success": True, "message": "Inquiry submitted successfully."}), 200
```

---

## 4. HTTP Security Headers

In `app/__init__.py`, an `@app.after_request` hook injects industry-standard protective headers:

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self';"
    )
    return response
```

---

## 5. Safe File Serving (`/resume`)

To prevent directory traversal attacks (`../../etc/passwd`), resume delivery strictly employs `send_from_directory`:

```python
@bp.route('/resume')
def download_resume():
    files_dir = os.path.join(current_app.root_path, 'static', 'files')
    as_attachment = request.args.get('download', '0') == '1'
    return send_from_directory(
        files_dir,
        'resume.pdf',
        as_attachment=as_attachment,
        mimetype='application/pdf'
    )
```
`send_from_directory` is guaranteed by Werkzeug to raise a `NotFound` error if any path traversal escape is attempted.

---

## 6. Secret Key Management

- A default development key is provided only when running in non-production environments with an explicit warning.
- In `ProductionConfig`, an explicit check asserts that `SECRET_KEY` is provided from the environment. If missing, the app refuses to boot, preventing weak session signatures.
