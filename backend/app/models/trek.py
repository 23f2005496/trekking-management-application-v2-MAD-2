from app import db

class Trek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    slots = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Open", nullable=False)
    image = db.Column(db.String(100), nullable=True)

    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)

    bookings = db.relationship('Booking', backref='trek', lazy="dynamic", cascade="all, delete-orphan")