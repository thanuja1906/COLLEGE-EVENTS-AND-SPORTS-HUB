from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, time
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_faculty = db.Column(db.Boolean, default=False)

    bookings = db.relationship('Booking', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_student(self):
        return not self.is_faculty

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    court_number = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cancelled_at = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint('court_number', 'start_time', 'booking_date', name='unique_booking_slot'),
    )

    def can_cancel(self):
        from datetime import datetime, timedelta
        booking_datetime = datetime.combine(self.booking_date, self.start_time)
        return datetime.now() < (booking_datetime - timedelta(minutes=15))

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100))
    max_participants = db.Column(db.Integer)
    registration_deadline = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    event_type = db.Column(db.String(20))
    gallery_images = db.Column(db.Text, default='[]')

    def __init__(self, **kwargs):
        super(Event, self).__init__(**kwargs)
        if self.gallery_images:
            self.gallery_images = json.dumps(self.gallery_images) if isinstance(self.gallery_images, list) else self.gallery_images
