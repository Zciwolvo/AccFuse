from flask import request, jsonify, make_response, current_app as app, url_for, render_template, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_jwt_extended import create_access_token, set_access_cookies
from datetime import datetime, timedelta
import requests
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

    # Create a nicely formatted HTML email
    msg = Message('Email Verification', recipients=[data['email']])
    msg.html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border: 1px solid #ddd; border-radius: 8px;">
            <tr>
                <td style="padding: 20px; text-align: center; background-color: #007bff; color: #ffffff; border-radius: 8px 8px 0 0;">
                    <h1 style="margin: 0;">Welcome to AccFuse</h1>
                </td>
            </tr>
            <tr>
                <td style="padding: 20px; color: #333;">
                    <p>Hi <strong>{data['username']}</strong>,</p>
                    <p>Thank you for registering with us! To complete your registration, please verify your email address by clicking the button below:</p>
                    <p style="text-align: center;">
                        <a href="{verification_url}" style="background-color: #007bff; color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 5px; font-size: 16px;">
                            Verify Email
                        </a>
                    </p>
                    <p>If the button above does not work, you can also copy and paste the following URL into your browser:</p>
                    <p style="word-wrap: break-word; color: #007bff;">{verification_url}</p>
                    <p>Welcome aboard!<br>AccFuse Team</p>
                </td>
            </tr>
            <tr>
                <td style="padding: 10px; text-align: center; background-color: #f4f4f4; color: #888; font-size: 12px;">
                    © {datetime.now().year} AccFuse. All rights reserved.
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
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

    # Verify reCAPTCHA
    recaptcha_response = data.get('recaptcha')
    recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
    recaptcha_payload = {
        'secret': app.config['RECAPTCHA_KEY'],
        'response': recaptcha_response
    }
    recaptcha_result = requests.post(recaptcha_verify_url, data=recaptcha_payload).json()

    if not recaptcha_result.get('success'):
        return jsonify({'message': 'reCAPTCHA verification failed. Please try again.'}), 400

    # Check user credentials
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login failed. Check credentials.'}), 401

    if not user.verified:
        return jsonify({'message': 'Email not verified. Please verify your email first.'}), 403

    # Create JWT token
    access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(minutes=30))
    response = make_response(jsonify({'message': 'Login successful!'}))
    set_access_cookies(response, access_token)

    return response

@user.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        # Render a form for entering the email address
        return render_template('forgot_password.html')

    # Handle the POST request to initiate password reset
    data = request.form
    email = data.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'No account found with this email.'}), 404

    # Generate and send a password reset token (implementation omitted for brevity)
    #send_password_reset_email(user)
    return jsonify({'message': 'Password reset email sent.'}), 200

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
