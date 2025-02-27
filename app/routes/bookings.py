from flask import Blueprint, jsonify, request
from app.models import Booking, Room, User
from app import db
from typing import List, Dict, Union

bp = Blueprint('bookings', __name__)

def validate_and_create_booking(data: Dict) -> Union[Dict, tuple]:
    # Validate required fields
    required_fields = ['roomId', 'date', 'timeSlot', 'userName', 'purpose']
    if not all(field in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400
    
    # Validate room exists
    room = Room.query.get(data['roomId'])
    if not room:
        return {'error': f'Room {data["roomId"]} not found'}, 404
    
    # Check if timeslot is already booked
    existing_booking = Booking.query.filter_by(
        room_id=data['roomId'],
        date=data['date'],
        time_slot=data['timeSlot']
    ).first()
    
    if existing_booking:
        return {'error': f'Time slot for room {data["roomId"]} on {data["date"]} at {data["timeSlot"]} is already booked'}, 409
    
    # Create new booking
    new_booking = Booking(
        room_id=data['roomId'],
        date=data['date'],
        time_slot=data['timeSlot'],
        user_name=data['userName'],
        purpose=data['purpose']
    )
    
    return new_booking

@bp.route('/bookings', methods=['GET'])
def get_bookings():
    # Get query parameters
    room_id = request.args.get('roomId')
    date = request.args.get('date')
    user_email = request.args.get('user')
    
    # Start with base query
    query = Booking.query
    
    # Apply filters if provided
    if room_id:
        query = query.filter_by(room_id=room_id)
    if date:
        query = query.filter_by(date=date)
    if user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            query = query.filter_by(user_id=user.id)
        else:
            return jsonify([])  # Return empty list if user not found
    
    bookings = query.all()
    return jsonify([{
        'id': str(booking.id),
        'roomId': str(booking.room_id),
        'date': booking.date,
        'timeSlot': booking.time_slot,
        'userName': booking.user_name,
        'purpose': booking.purpose
    } for booking in bookings]), 200

@bp.route('/bookings', methods=['POST'])
def create_booking():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    # Handle single booking
    if isinstance(data, dict):
        result = validate_and_create_booking(data)
        if isinstance(result, tuple):  # Error case
            return jsonify(result[0]), result[1]
        
        new_booking = result
        db.session.add(new_booking)
        db.session.commit()
        
        return jsonify({
            'id': str(new_booking.id),
            'roomId': str(new_booking.room_id),
            'date': new_booking.date,
            'timeSlot': new_booking.time_slot,
            'userName': new_booking.user_name,
            'purpose': new_booking.purpose
        }), 201
    
    # Handle multiple bookings
    elif isinstance(data, list):
        if not data:
            return jsonify({'error': 'Empty booking list'}), 400
        
        bookings_response = []
        errors = []
        
        for booking_data in data:
            result = validate_and_create_booking(booking_data)
            if isinstance(result, tuple):  # Error case
                errors.append({
                    'booking': booking_data,
                    'error': result[0]['error']
                })
            else:
                bookings_response.append(result)
        
        # If there are any errors, rollback and return the errors
        if errors:
            return jsonify({
                'error': 'Some bookings could not be created',
                'details': errors
            }), 400
        
        # All bookings are valid, commit them
        for booking in bookings_response:
            db.session.add(booking)
        db.session.commit()
        
        return jsonify([{
            'id': str(booking.id),
            'roomId': str(booking.room_id),
            'date': booking.date,
            'timeSlot': booking.time_slot,
            'userName': booking.user_name,
            'purpose': booking.purpose
        } for booking in bookings_response]), 201
    
    else:
        return jsonify({'error': 'Invalid request format'}), 400

@bp.route('/bookings/<id>', methods=['GET'])
def get_booking(id):
    booking = Booking.query.get_or_404(id)
    return jsonify({
        'id': str(booking.id),
        'roomId': str(booking.room_id),
        'date': booking.date,
        'timeSlot': booking.time_slot,
        'userName': booking.user_name,
        'purpose': booking.purpose
    }), 200

@bp.route('/bookings/<id>', methods=['DELETE'])
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return '', 204 