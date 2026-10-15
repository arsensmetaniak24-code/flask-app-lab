from dotenv import load_dotenv
from flask import Flask

load_dotenv("../.flaskenv")

app = Flask(__name__)
app.config.from_prefixed_env()

from . import views

from .users import users_bp
app.register_blueprint(users_bp)