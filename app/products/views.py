from datetime import datetime
import uuid
from pathlib import Path

from flask import request, redirect, url_for, render_template, abort, flash
from .db import get_products_table

from . import products_bp
from .forms import ProductForm


@products_bp.route('/')
def all_products():

    return render_template("products.html", title="All Products", products=get_all_products())

@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    for product in get_all_products():
        if product["id"] == product_id:
            return render_template("product.html", title="Product", product=product)
    abort(404)

@products_bp.route('/add', methods=["GET", "POST"])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        filepath = save_image(form.image.data) if form.image.data else ''
        product = {
            "name": form.name.data,
            "content": form.content.data,
            "price": round(float(form.price.data), 2),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": filepath,
            "created_at": datetime.now().isoformat(timespec='seconds')
        }
        product_id = get_products_table().insert(product)
        flash("Product added successfully", "success")
        return redirect(url_for("products.product_detail", product_id=product_id))

    if (request.method == 'POST'):
        flash("Invalid form submission", "warning")

    return render_template("product_form.html", title="Add Product", form=form)


def get_all_products():
    products = []
    for product in get_products_table().all():
        products.append({**product, 'id': product.doc_id})
    return products

def save_image(file):
    ext = Path(file.filename).suffix.lower()
    filename = f"{uuid.uuid4()}{ext}"
    path = Path(products_bp.static_folder, "uploads", filename)
    file.save(path)
    return f"uploads/{filename}"
