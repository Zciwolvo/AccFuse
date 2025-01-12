# app/__init__.py
from flask import Flask, render_template, jsonify
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_cors import CORS

mail = Mail()
jwt = JWTManager()
cors = CORS()


def create_app(test=False):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'igor.gawlowicz@gmail.com' 
    app.config['MAIL_PASSWORD'] = 'lzdcztxbkzieszxj'
    app.config['MAIL_RECEIVER'] = 'igor.gawlowicz@gmail.com' 
    app.config['MAIL_DEFAULT_SENDER'] = ('AccFuse', 'igor.gawlowicz@gmail.com')
    
    # JWT Configuration
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_ACCESS_COOKIE_NAME'] = "token"
    
    app.config['RECAPTCHA_KEY'] = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
    
    if test:
        app.config["MAIL_SUPPRESS_SEND"] = True
        app.config["JWT_COOKIE_SECURE"] = False
    
    # Register blueprints
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    
    from .tos import tos as tos_blueprint
    app.register_blueprint(tos_blueprint)

    from .privacy import privacy as privacy_blueprint
    app.register_blueprint(privacy_blueprint)
    
    from .contact import contact as contact_blueprint
    app.register_blueprint(contact_blueprint)
    
    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")
    
    from .help import help_page as help_page_blueprint
    app.register_blueprint(help_page_blueprint)
    
    from .database import init_app
    init_app(app, test)
    
    # Initialize extensions
    mail.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    
    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/user")
    
    
    #Error handling
    

    return app
