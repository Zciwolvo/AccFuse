import pytest
from unittest.mock import patch
from app.database import database as db
from app.database.Models.User import User

@patch('app.user.controller.send_verification_email')  # Adjust mock to actual email function
def test_register(mock_mail_send, client, app):
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    }

    response = client.post('/user/register', json=data)
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

    # Check the user is added to the database
    with app.app_context():
        user = User.query.filter_by(email=data['email']).first()
        assert user is not None
        assert user.username == data['username']

    # Ensure mail is sent
    mock_mail_send.assert_called_once_with(user)



@patch('app.user.controller.login')  # Mock the reCAPTCHA verification request
def test_login(mock_post, client, app):
    # Mock successful reCAPTCHA response
    mock_post.return_value.json.return_value = {'success': True}

    # Create a user in the test database
    with app.app_context():
        from werkzeug.security import generate_password_hash
        user = User(username='testuser', email='testuser@example.com', password=generate_password_hash('password123'))
        db.session.add(user)
        db.session.commit()

    # Attempt to login
    data = {
        'email': 'testuser@example.com',
        'password': 'password123',
        'recaptcha': 'dummy-recaptcha-response'
    }
    response = client.post('/user/login', json=data)
    assert response.status_code == 200
    assert b'Login successful' in response.data



@patch('app.user.controller.forgot_password')
def test_forgot_password(mock_mail_send, client, app):
    with app.app_context():
        user = User(username='testuser', email='testuser@example.com')
        db.session.add(user)
        db.session.commit()

    response = client.post('/user/forgot-password', json={'email': 'testuser@example.com'})
    assert response.status_code == 200
    assert b'Password reset email sent' in response.data

    # Ensure mail is sent
    mock_mail_send.assert_called_once()


@patch('app.user.controller.change_password')
def test_change_password(mock_jwt_decode, client, app):
    # Mock decoding the JWT token
    mock_jwt_decode.return_value = {'user_id': 1}

    with app.app_context():
        from werkzeug.security import generate_password_hash
        user = User(username='testuser', email='testuser@example.com', password=generate_password_hash('oldpassword'))
        db.session.add(user)
        db.session.commit()

    data = {
        'old_password': 'oldpassword',
        'new_password': 'newpassword123'
    }
    response = client.put('/user/change-password', json=data)
    assert response.status_code == 200
    assert b'Password updated successfully' in response.data

    # Verify the password was changed
    with app.app_context():
        user = User.query.get(1)
        from werkzeug.security import check_password_hash
        assert check_password_hash(user.password, 'newpassword123')
