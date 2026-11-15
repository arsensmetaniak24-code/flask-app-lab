from flask import Blueprint

posts_bp = Blueprint(
    "posts",
    __name__,
    template_folder="templates/posts",
    url_prefix='/post',
    static_folder="static"
)

from . import views