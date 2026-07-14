from app import db
from datetime import datetime
from pytz import timezone

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone("Asia/Kolkata")), nullable=False)
    status = db.Column(db.String(20), default="Not Booked", nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)