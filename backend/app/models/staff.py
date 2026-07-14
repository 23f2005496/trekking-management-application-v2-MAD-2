from app import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=True)
    status = db.Column(db.String(20), default="Active", nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    
    assigned_treks = db.relationship('Trek', backref='staff', lazy="dynamic", cascade="all, delete-orphan")