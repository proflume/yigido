"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from app import db, redis_client
from app.models import User
from app.utils.validators import validate_email, validate_password
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validation
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not email or not validate_email(email):
        return jsonify({'error': 'Invalid email address'}), 400
    
    if not username or len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    
    if not validate_password(password):
        return jsonify({'error': 'Password must be at least 8 characters with uppercase, lowercase, and number'}), 400
    
    # Check if user exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 409
    
    # Create user
    user = User(
        email=email,
        username=username,
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    # Generate tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict(include_email=True),
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 201


@bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username_or_email = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username_or_email or not password:
        return jsonify({'error': 'Username/email and password required'}), 400
    
    # Find user by username or email
    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is disabled'}), 403
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Generate tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(include_email=True),
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token}), 200


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (blacklist token)"""
    jti = get_jwt()['jti']
    # Add token to blacklist in Redis
    redis_client.setex(f'blacklist:{jti}', 3600, '1')
    return jsonify({'message': 'Logout successful'}), 200


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict(include_email=True)}), 200
