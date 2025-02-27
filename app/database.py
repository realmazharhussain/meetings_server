from app import db
from app.models import User, Room
from werkzeug.security import generate_password_hash

def init_db(app):
    with app.app_context():
        db.create_all()
        init_default_user()
        init_rooms()

def init_default_user():
    if not User.query.filter_by(email='user@example.com').first():
        default_user = User(
            email='user@example.com',
            password=generate_password_hash('password123')
        )
        db.session.add(default_user)
        db.session.commit()

def init_rooms():
    default_rooms = [
        {
            "name": "Brainstorm Room",
            "capacity": 4,
            "amenities": ["Whiteboard", "TV", "HDMI Cable"],
            "image": "/placeholder.svg?height=300&width=500"
        },
        {
            "name": "Conference Room",
            "capacity": 10,
            "amenities": ["Projector", "Whiteboard", "Video Conference"],
            "image": "/placeholder.svg?height=300&width=500"
        },
        {
            "name": "Quiet Space",
            "capacity": 2,
            "amenities": ["Soundproof", "Comfortable Chairs"],
            "image": "/placeholder.svg?height=300&width=500"
        },
        {
            "name": "Innovation Lab",
            "capacity": 8,
            "amenities": ["Whiteboard", "Projector", "Modular Furniture"],
            "image": "/placeholder.svg?height=300&width=500"
        }
    ]
    
    for room_data in default_rooms:
        if not Room.query.filter_by(name=room_data["name"]).first():
            room = Room(
                name=room_data["name"],
                capacity=room_data["capacity"],
                amenities=",".join(room_data["amenities"]),
                image=room_data["image"]
            )
            db.session.add(room)
    db.session.commit()