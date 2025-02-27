from flask import Blueprint, jsonify
from app.models import Room

bp = Blueprint('rooms', __name__)

@bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    rooms_list = []
    for room in rooms:
        rooms_list.append({
            "id": str(room.id),
            "name": room.name,
            "capacity": room.capacity,
            "amenities": room.amenities.split(","),
            "image": room.image
        })
    return jsonify(rooms_list), 200

@bp.route('/rooms/<id>', methods=['GET'])
def get_room(id):
    room = Room.query.get_or_404(id)
    return jsonify({
        "id": str(room.id),
        "name": room.name,
        "capacity": room.capacity,
        "amenities": room.amenities.split(","),
        "image": room.image
    }), 200