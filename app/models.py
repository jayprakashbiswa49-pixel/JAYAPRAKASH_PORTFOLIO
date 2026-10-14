from datetime import datetime, timezone
from app import db


class ContactInquiry(db.Model):
    """Optional persistence model for user inquiries via contact form."""
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
