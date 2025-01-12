import pytest
from app import create_app
from app.database import database as db

@pytest.fixture
def app():
    # Set up the Flask app with test configuration
    app = create_app(test=True)  # Ensure your app supports 'testing' config
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for tests
    
    with app.app_context():
        db.create_all()  # Create the database tables
    
    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()  # Clean up the database

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
