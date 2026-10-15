from flask import request, redirect, url_for, render_template

from .. import app
from . import products_bp


products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 1200,
        "content": "Потужний ноутбук з процесором Intel Core i7, 16 ГБ оперативної пам’яті та SSD на 512 ГБ."
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 800,
        "content": "Смартфон із 6.5-дюймовим OLED-дисплеєм, подвійною камерою та акумулятором на 5000"
    },
    {
        "id": 3,
        "name": "PC",
        "price": 1800,
        "content": "Настільний комп’ютер для ігор або роботи з графікою: RTX 4070, 32 ГБ RAM, 1 ТБ SSD."
    }
]

@products_bp.route('/')
def all_products():
    return render_template("products.html", title="All Products", products=products)

@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    for product in products:
        if product["id"] == product_id:
            return render_template("product.html", title="Product", product=product)
    return None
