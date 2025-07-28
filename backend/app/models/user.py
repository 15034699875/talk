from .. import db
from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    avatar_url = db.Column(db.String(255))
    points = db.Column(db.Integer, default=0)
    exp = db.Column(db.BigInteger, default=0)
    role = db.Column(Enum('user', 'admin'), default='user')
    email = db.Column(db.String(120), unique=True)
    is_banned = db.Column(db.Boolean, default=False) 