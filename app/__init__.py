from dotenv import load_dotenv
from flask import Flask
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".flaskenv")

app = Flask(__name__)
app.config.from_prefixed_env()

from . import views

from .users import users_bp
app.register_blueprint(users_bp)

from .products import products_bp
app.register_blueprint(products_bp)