from app import db
import datetime

class Token(db.Model):
    token = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expires = db.Column(db.DateTime, nullable=False)