from app import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # Format: YYYY-MM-DD
    time_slot = db.Column(db.String(20), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(200), nullable=False)