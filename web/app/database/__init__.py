from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Remove the db Blueprint; use this database for the app
database = SQLAlchemy()
migrate = Migrate()

def init_app(app):
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost:3306/AccFuse'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy and Migrate with app
    database.init_app(app)
    migrate.init_app(app, database)

    # Import models to register them with SQLAlchemy
    from .Models import User, Bank, Account, Balance, Transaction, BankTransactionCode, RelatedParty
    with app.app_context():
        database.create_all()
