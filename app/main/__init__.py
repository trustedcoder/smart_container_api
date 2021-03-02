from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config_by_name
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    from app import blueprint

    app.register_blueprint(blueprint)

    db.init_app(app)
    migrate = Migrate(app, db)
    return app
