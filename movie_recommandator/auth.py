from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
import re  # ✅ For email validation

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    print(f"DEBUG: /auth/signup route reached with method: {request.method}")
    data = request.get_json()
    print(f"DEBUG: Received data: {data}")
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'error': 'Missing fields'}), 400

    # ✅ Email format validation
    email_pattern = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_pattern, email):
        return jsonify({'error': 'Invalid email format'}), 400

    # ✅ Check for existing user
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'User already exists'}), 400

    # ✅ Create and save user
    password_hash = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    # ✅ Auto-login the new user
    login_user(new_user)

    return jsonify({'message': 'User created and logged in successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({'error': 'Missing credentials'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    login_user(user)
    return jsonify({'message': 'Logged in successfully'})

@auth_bp.route('/logout', methods=['POST'])
#@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@auth_bp.route('/current_user', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({'username': current_user.username, 'email': current_user.email})
    return jsonify({'username': None})
