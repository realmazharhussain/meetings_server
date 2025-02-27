from flask import Blueprint, jsonify
from app.models import Room

bp = Blueprint('rooms', __name__)

def serialize_room(room):
    return {
        "id": str(room.id),
        "name": room.name,
        "capacity": room.capacity,
        "amenities": room.amenities.split(","),
        "image": room.image,
        "bookings": [{
            'id': str(booking.id),
            'date': booking.date,
            'timeSlot': booking.time_slot,
            'userName': booking.user_name,
            'purpose': booking.purpose
        } for booking in room.bookings]
    }

@bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([serialize_room(room) for room in rooms]), 200

@bp.route('/rooms/<id>', methods=['GET'])
def get_room(id):
    room = Room.query.get_or_404(id)
    return jsonify(serialize_room(room)), 200