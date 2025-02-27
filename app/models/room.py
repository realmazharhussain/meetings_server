from app import db

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    amenities = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    bookings = db.relationship('Booking', backref='room', lazy=True)