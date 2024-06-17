import pytest
from agrihire import create_app

@pytest.fixture(scope='session')
def app():
    # Create a test version of your Flask application
    app = create_app()
    
    app.config.update({
        "TESTING": True,
    })
    
    # Additional setup, if needed
    # For example, you might want to initialize a test database here
        
    yield app
    
@pytest.fixture
def client(app):
    app.config["WTF_CSRF_ENABLED"] = False
    # Create a test client using the test version of your Flask application
    with app.test_client() as client:
        yield client

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
