from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from app import db
from app.models import User, Token
from app.auth import generate_token

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing email or password'}), 400
    
    email = data['email']
    password = data['password']

    # Find user by email
    user = User.query.filter_by(email=email).first()

    # If user doesn't exist, create one
    if not user:
        user = User(
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
    # If user exists, verify password
    elif not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid password'}), 401

    # Create new token
    token = Token(
        token=generate_token(),
        user_id=user.id,
        expires=datetime.datetime.utcnow() + datetime.timedelta(days=30)
    )
    db.session.add(token)
    db.session.commit()

    # Create response with cookie
    response = make_response(jsonify({'message': 'Login successful'}), 200)
    response.set_cookie(
        'session_token',
        token.token,
        httponly=True,
        secure=True,  # Only send over HTTPS
        samesite='Strict',
        expires=token.expires
    )

    return response