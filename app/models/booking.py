from app import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # Format: YYYY-MM-DD
    time_slot = db.Column(db.String(11), nullable=False)  # HH:MM-HH:MM
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)  # Display name for the booking
    purpose = db.Column(db.String(200), nullable=False)
    
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))