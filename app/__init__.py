from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import configs

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    configs[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
