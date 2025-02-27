from app import db
from app.models import User, Room
from werkzeug.security import generate_password_hash

def init_db(app):
    with app.app_context():
        db.create_all()
        init_users()
        init_rooms()

def init_users():
    if User.query.count() == 0:
        admin = User(
            email="admin@example.com",
            password=generate_password_hash("admin123")
        )
        db.session.add(admin)
        db.session.commit()

def init_rooms():
    if Room.query.count() == 0:
        rooms_data = [
            {
                "name": "Brainstorm Room",
                "capacity": 4,
                "amenities": "Whiteboard,TV,HDMI Cable",
                "image": "https://images.unsplash.com/photo-1517502884422-41eaead166d4?w=500&h=300&auto=format&fit=crop&q=80"
            },
            {
                "name": "Conference Room",
                "capacity": 10,
                "amenities": "Projector,Whiteboard,Video Conference",
                "image": "https://images.unsplash.com/photo-1431540015161-0bf868a2d407?w=500&h=300&auto=format&fit=crop&q=80"
            },
            {
                "name": "Quiet Space",
                "capacity": 2,
                "amenities": "Soundproof,Comfortable Chairs",
                "image": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=500&h=300&auto=format&fit=crop&q=80"
            },
            {
                "name": "Innovation Lab",
                "capacity": 8,
                "amenities": "Whiteboard,Projector,Modular Furniture",
                "image": "https://images.unsplash.com/photo-1577412647305-991150c7d163?w=500&h=300&auto=format&fit=crop&q=80"
            }
        ]

        for room_data in rooms_data:
            room = Room(
                name=room_data["name"],
                capacity=room_data["capacity"],
                amenities=room_data["amenities"],
                image=room_data["image"]
            )
            db.session.add(room)
        
        db.session.commit()