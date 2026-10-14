from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    """Secure contact form with CSRF protection, input constraints, and honeypot."""

    name = StringField(
        'Full Name',
        validators=[
            DataRequired(message='Please provide your name.'),
            Length(min=2, max=80, message='Name must be between 2 and 80 characters.')
        ],
        render_kw={'placeholder': 'e.g. Alex Morgan', 'autocomplete': 'name'}
    )

    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message='Please provide your email address.'),
            Email(message='Please provide a valid email address.'),
            Length(max=120, message='Email address is too long (maximum 120 characters).')
        ],
        render_kw={'placeholder': 'e.g. alex@example.com', 'autocomplete': 'email'}
    )

    subject = StringField(
        'Subject',
        validators=[
            DataRequired(message='Please provide a subject.'),
            Length(min=3, max=150, message='Subject must be between 3 and 150 characters.')
        ],
        render_kw={'placeholder': 'e.g. Project Collaboration or Internship Inquiry'}
    )

    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message='Please enter your message.'),
            Length(min=10, max=2000, message='Message must be between 10 and 2000 characters.')
        ],
        render_kw={
            'placeholder': 'Tell me about your project, idea, or how we might collaborate...',
            'rows': 5
        }
    )

    # Honeypot field: invisible to humans, attracts spam bots
    hp_website = StringField(
        'Website',
        validators=[Length(max=100)],
        render_kw={'tabindex': '-1', 'autocomplete': 'off'}
    )

    submit = SubmitField('Send Message')
