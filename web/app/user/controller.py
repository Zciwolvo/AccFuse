from flask import request, jsonify, make_response, current_app as app, url_for, render_template, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_jwt_extended import create_access_token, set_access_cookies
from datetime import datetime, timedelta
import jwt
from flask_mail import Message
from ..database.Models.User import User
from ..database import database as db
from . import user
from app import mail

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirmation')

def confirm_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirmation', max_age=expiration)
        return email
    except (SignatureExpired, BadSignature):
        return None

@user.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()

    # Generate token and send verification email
    token = generate_verification_token(data['email'])
    verification_url = url_for('user.verify_email', token=token, _external=True)
    
    msg = Message('Email Verification', recipients=[data['email']])
    msg.body = f'Please verify your email by clicking the following link: {verification_url}'
    mail.send(msg)

    return jsonify({'message': 'User registered successfully! Please check your email to verify your account.'}), 201

@user.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    email = confirm_verification_token(token)
    if not email:
        return jsonify({'message': 'The verification link is invalid or has expired.'}), 400

    user = User.query.filter_by(email=email).first_or_404()
    user.verified = True
    db.session.commit()

    return render_template('verification.html')

@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login failed. Check credentials.'}), 401

    if not user.verified:
        return jsonify({'message': 'Email not verified. Please verify your email first.'}), 403

    # Use create_access_token with the user's ID as the identity (this sets the `sub` claim)
    access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(minutes=30))

    # Create a response and set the JWT access token as an HTTP-only cookie
    response = make_response(jsonify({'message': 'Login successful!'}))
    set_access_cookies(response, access_token)

    return response

@user.route('/logout')
def logout():
    # Create a response to redirect the user to the home page
    resp = make_response(redirect(url_for('home.index')))
    
    # Remove the JWT token from cookies
    resp.delete_cookie('token')

    return resp

@user.route('/change-password', methods=['PUT'])
def change_password():
    data = request.get_json()
    user_id = jwt.decode(request.cookies.get('token'), app.config['SECRET_KEY'], algorithms=["HS256"])['user_id']
    user = User.query.get(user_id)

    if not user or not check_password_hash(user.password, data['old_password']):
        return jsonify({'message': 'Password change failed. Incorrect current password.'}), 400

    user.password = generate_password_hash(data['new_password'], method='pbkdf2:sha256')
    db.session.commit()

    return jsonify({'message': 'Password updated successfully!'})

@user.route('/update-username', methods=['PUT'])
def update_username():
    data = request.get_json()
    user_id = jwt.decode(request.cookies.get('token'), app.config['SECRET_KEY'], algorithms=["HS256"])['user_id']
    user = User.query.get(user_id)

    if user:
        user.username = data['username']
        db.session.commit()
        return jsonify({'message': 'Username updated successfully!'})
    else:
        return jsonify({'message': 'User not found.'}), 404
