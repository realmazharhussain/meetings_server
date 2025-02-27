from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
import datetime
from app import db
from app.models import User, Token

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400
    
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    
    if user:  # Login flow
        if not check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid email or password'}), 401
    else:  # Registration flow
        # Create new user
        user = User(
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
    
    # Generate token for the user
    token = secrets.token_urlsafe(32)
    token_obj = Token(
        token=token,
        user_id=user.id,
        expires=datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    )
    db.session.add(token_obj)
    db.session.commit()
    
    return jsonify({'userID': token}), 200