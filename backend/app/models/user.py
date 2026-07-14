from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=True)
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="Active", nullable=False)

    bookings = db.relationship('Booking', backref='user', lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.full_name}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def get_all_users(cls):
        return cls.query.filter(cls.role != "admin").all()
