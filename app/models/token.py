from app import db
import datetime

class Token(db.Model):
    token = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tokens', lazy=True))
    expires = db.Column(db.DateTime, nullable=False)