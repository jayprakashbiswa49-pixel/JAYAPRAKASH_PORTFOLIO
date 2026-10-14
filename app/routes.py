import os
import hashlib
from flask import (
    Blueprint, render_template, request, jsonify, flash, redirect,
    url_for, current_app, send_from_directory, abort
)
from app.forms import ContactForm
from app.portfolio_data import (
    PROFILE_DATA, SKILL_GROUPS, PROJECTS,
    PROJECT_CATEGORIES, EDUCATION, CERTIFICATIONS
)
from app.services.email_service import EmailService

bp = Blueprint('routes', __name__)


@bp.route('/', methods=['GET'])
def index():
    """Renders the main developer portfolio with complete Jinja2 SSR context."""
    form = ContactForm()
    return render_template(
        'index.html',
        profile=PROFILE_DATA,
        skill_groups=SKILL_GROUPS,
        projects=PROJECTS,
        categories=PROJECT_CATEGORIES,
        education=EDUCATION,
        certifications=CERTIFICATIONS,
        form=form
    )


@bp.route('/api/index', methods=['GET'], endpoint='vercel_index')
def vercel_index_alias():
    """Fallback route for Vercel when requests arrive with literal /api/index path."""
    return index()


@bp.route('/api/index/static/<path:filename>', methods=['GET'], endpoint='vercel_static')
def vercel_static_fallback(filename):
    """Fallback route for static assets when Vercel rewrites with an /api/index prefix."""
    static_dir = os.path.join(current_app.root_path, 'static')
    return send_from_directory(static_dir, filename)




@bp.route('/resume', methods=['GET'])
def download_resume():
    """Serves Jayaprakash Biswal's actual PDF resume with security checks."""
    files_dir = os.path.join(current_app.root_path, 'static', 'files')
    filename = 'resume.pdf'

    if not os.path.isfile(os.path.join(files_dir, filename)):
        current_app.logger.error(f"Resume file not found at {files_dir}/{filename}")
        abort(404)

    # Check if user requested direct attachment download vs inline viewer
    as_attachment = request.args.get('download', '0') in ('1', 'true')
    return send_from_directory(
        files_dir,
        filename,
        as_attachment=as_attachment,
        download_name='Jayaprakash_Biswal_Resume.pdf',
        mimetype='application/pdf'
    )


@bp.route('/contact', methods=['POST'])
def submit_contact():
    """Validates and processes contact form submissions via AJAX or standard POST."""
    is_ajax = request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.is_json:
        form = ContactForm(data=request.get_json())
    else:
        form = ContactForm()

    # Honeypot spam defense check
    if form.hp_website.data:
        current_app.logger.warning("Spam bot caught via honeypot field.")
        # Silent success response to not alert the spam crawler
        if is_ajax:
            return jsonify({'success': True, 'message': 'Thank you! Your message has been received.'}), 200
        flash('Thank you! Your message has been received.', 'success')
        return redirect(url_for('routes.index', _anchor='contact'))

    if form.validate_on_submit():
        name = form.name.data.strip()
        email = form.email.data.strip()
        subject = form.subject.data.strip()
        message = form.message.data.strip()

        # Extract client IP for security auditing
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr or 'unknown')
        if ',' in client_ip:
            client_ip = client_ip.split(',')[0].strip()

        # Dispatch notification via EmailService
        EmailService.send_inquiry(name, email, subject, message, client_ip)

        # Optional database persistence
        if current_app.config.get('ENABLE_DB'):
            try:
                from app import db
                from app.models import ContactInquiry
                ip_hash = hashlib.sha256(client_ip.encode('utf-8')).hexdigest()
                inquiry = ContactInquiry(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message,
                    ip_hash=ip_hash
                )
                db.session.add(inquiry)
                db.session.commit()
            except Exception as e:
                current_app.logger.error(f"Database persistence failed: {e}")

        success_msg = 'Thank you, your message has been sent successfully! I will get in touch with you shortly.'
        if is_ajax:
            return jsonify({'success': True, 'message': success_msg}), 200

        flash(success_msg, 'success')
        return redirect(url_for('routes.index', _anchor='contact'))

    # Form validation failed
    error_msg = 'Please correct the highlighted errors before submitting.'
    if is_ajax:
        return jsonify({
            'success': False,
            'message': error_msg,
            'errors': form.errors
        }), 400

    flash(error_msg, 'danger')
    return render_template(
        'index.html',
        profile=PROFILE_DATA,
        skill_groups=SKILL_GROUPS,
        projects=PROJECTS,
        categories=PROJECT_CATEGORIES,
        education=EDUCATION,
        certifications=CERTIFICATIONS,
        form=form
    ), 400


@bp.route('/health', methods=['GET'])
def health_check():
    """Minimal deployment health check route for monitoring services and Render."""
    return jsonify({
        'status': 'ok',
        'app': 'Jayaprakash Biswal Portfolio',
        'version': '1.0.0',
        'debug': current_app.debug
    }), 200
