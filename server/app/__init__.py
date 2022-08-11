from flask import Flask
from app.extensions import db, cors
from app.config import Config
from app.blueprints import user, roles


def create_app(config=Config):
    app = Flask("app")
    app.config.from_object(config)

    extensions(app)
    # app.register_blueprint(post)
    app.register_blueprint(roles)
    app.register_blueprint(user)

    return app


def extensions(app):
    db.init_app(app)
    cors.init_app(app)
