"""Database models and database setup using SQLAlchemy."""

from datetime import date

from flask_sqlalchemy import SQLAlchemy

# In production we will configure this with PostgreSQL

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'council', 'hotel', 'admin'


class Hotel(db.Model):
    """Registered hotel property."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User")

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel = db.Column(db.String(100), nullable=False)
    room_id = db.Column(db.String(50), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    price = db.Column(db.Float, nullable=True)
    date_available = db.Column(db.Date, default=date.today)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nights = db.Column(db.Integer, default=1)
    total_cost = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default='booked')


class Session(db.Model):
    """Persistent auth tokens."""

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


def init_db(app):
    """Initialize database with the given Flask app."""
    db.init_app(app)
    with app.app_context():
        db.create_all()

