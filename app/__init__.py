from dotenv import load_dotenv
from flask import Flask
from pathlib import Path
import logging

load_dotenv(Path(__file__).parent.parent / ".flaskenv")

app = Flask(__name__)
app.config.from_prefixed_env()

logger = logging.getLogger(__name__)
handler = logging.FileHandler(filename=Path(__file__).parent.parent / "logs/contacts.log", mode="a")
handler.setFormatter(logging.Formatter("%(asctime)s : %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

from . import views

from .users import users_bp
app.register_blueprint(users_bp)

from .products import products_bp
app.register_blueprint(products_bp)