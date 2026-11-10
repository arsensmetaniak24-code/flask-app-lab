from flask import current_app
from tinydb import TinyDB
from datetime import datetime

def seed_products():
    t = get_products_table()
    if len(t) == 0:
        t.insert_multiple([
            {
                "name": "Laptop",
                "price": 1200,
                "content": "Потужний ноутбук з процесором Intel Core i7, 16 ГБ оперативної пам’яті та SSD на 512 ГБ.",
                "created_at": datetime.now().isoformat(timespec="seconds")
            },
            {
                "name": "Phone",
                "price": 800,
                "content": "Смартфон із 6.5-дюймовим OLED-дисплеєм, подвійною камерою та акумулятором на 5000",
                "created_at": datetime.now().isoformat(timespec="seconds")
            },
            {
                "name": "PC",
                "price": 1800,
                "content": "Настільний комп’ютер для ігор або роботи з графікою: RTX 4070, 32 ГБ RAM, 1 ТБ SSD.",
                "created_at": datetime.now().isoformat(timespec="seconds")
            }
        ])

def get_products_table():
    path = current_app.config["PRODUCTS_DB"]
    if path.exists():
        db = TinyDB(path)
        return db.table("products")
    else:
        raise FileNotFoundError(f"Products database file not found at {path}")