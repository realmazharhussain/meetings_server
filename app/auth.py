from functools import wraps
from flask import request, jsonify
from app.models import Token
import datetime
import secrets

def generate_token() -> str:
    """Generate a secure random token string"""
    return secrets.token_urlsafe(32)

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_str = request.cookies.get('session_token')
        
        if not token_str:
            return jsonify({'error': 'Authentication required'}), 401
        
        token = Token.query.get(token_str)
        if not token:
            return jsonify({'error': 'Invalid token'}), 401
            
        if token.expires < datetime.datetime.utcnow():
            return jsonify({'error': 'Token expired'}), 401
        
        # Add token to request context
        request.token = token
        return f(*args, **kwargs)
    return decorated 