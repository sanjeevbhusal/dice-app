import pytest
from server import create_app
from server import TestConfig
from server import db


# create a client application
@pytest.fixture(scope="session")
def app():
    app = create_app(config=TestConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app


@pytest.fixture(scope="function")
def client(app):
    yield app.test_client()
