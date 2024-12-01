from flask import request, render_template, flash, redirect, url_for, current_app as app, make_response
from flask_mail import Message
import jwt
from . import home
from .. import mail 


@home.route('/')
def index():
    token = request.cookies.get('token')
    user_logged_in = False
    error_message = None
    
    if token:
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_logged_in = True
        except jwt.ExpiredSignatureError:
            error_message = "Your session has expired. Please log in again."
            resp = make_response(render_template('home.html', user_logged_in=user_logged_in, error_message=error_message))
            resp.delete_cookie('token')  
            return resp
        except jwt.InvalidTokenError:
            error_message = "Invalid token. Please log in again."
            resp = make_response(render_template('home.html', user_logged_in=user_logged_in, error_message=error_message))
            resp.delete_cookie('token') 
            return resp

    return render_template('home.html', user_logged_in=user_logged_in)

@home.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Create the email message
        msg = Message(subject=f"[Contact Us] {subject}",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_RECEIVER']]) 
        msg.body = f"""
        New message from your website contact form:

        Name: {name}
        Email: {email}
        Subject: {subject}

        Message:
        {message}
        """
        
        try:
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('home.contact'))
        except Exception as e:
            flash('An error occurred while sending your message. Please try again later.', 'danger')
            print(f"Mail sending error: {e}")
            return redirect(url_for('home.contact'))
    
    return render_template('contact.html')
