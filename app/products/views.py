from flask import request, redirect, url_for, render_template, abort
from .db import get_products_table

from . import products_bp


@products_bp.route('/')
def all_products():

    return render_template("products.html", title="All Products", products=get_all_products())

@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    for product in get_all_products():
        if product["id"] == product_id:
            return render_template("product.html", title="Product", product=product)
    abort(404)

def get_all_products():
    products = []
    for product in get_products_table().all():
        products.append({**product, 'id': product.doc_id})
    return products
