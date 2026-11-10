from flask import Blueprint

products_bp = Blueprint(
    'products',
    __name__,
    template_folder='templates/products',
    url_prefix='/products',
    static_folder='static'
)

from . import views