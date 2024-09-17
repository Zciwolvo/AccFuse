# app/__init__.py
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    
    from .tos import tos as tos_blueprint
    app.register_blueprint(tos_blueprint)

    from .privacy import privacy as privacy_blueprint
    app.register_blueprint(privacy_blueprint)
    
    from .contact import contact as contact_blueprint
    app.register_blueprint(contact_blueprint)
    
    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)
    
    from .help import help_page as help_page_blueprint
    app.register_blueprint(help_page_blueprint)
        


    return app