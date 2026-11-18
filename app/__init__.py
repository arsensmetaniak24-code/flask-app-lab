from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from .config import config_map

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

logger = logging.getLogger(__name__)

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    if not logger.handlers:
        handler = logging.FileHandler(filename=Path(__file__).parent.parent / "logs/contacts.log", mode="a")
        handler.setFormatter(logging.Formatter("%(asctime)s : %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    from .views import main_bp
    app.register_blueprint(main_bp)

    from .users import users_bp
    app.register_blueprint(users_bp)

    from .products import products_bp
    app.register_blueprint(products_bp)

    from .posts import posts_bp
    app.register_blueprint(posts_bp)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    if not app.config["TESTING"]:
        with app.app_context():
            from .products.db import seed_products
            seed_products()

    return app

