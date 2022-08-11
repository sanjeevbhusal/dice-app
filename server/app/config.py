from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get("SECRET_KEY")
    DEBUG = True


class TestConfig:
    SQLALCHEMY_DATABASE_URI = environ.get("TEST_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get("SECRET_KEY")
    TESTING = True
    SERVER_NAME = "localhost:5000"
    DEBUG = True
