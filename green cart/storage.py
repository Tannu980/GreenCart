

import json
import os

from .models import Customer, Admin, Product


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")


def _read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []                      
    except json.JSONDecodeError:
        print(f"Warning: {path} is corrupted. Starting with empty data.")
        return []


def _write_json(path, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_users():
    users = {}
    for entry in _read_json(USERS_FILE):
        user = Admin.from_dict(entry) if entry.get("role") == "admin" else Customer.from_dict(entry)
        users[user.username] = user
    return users


def save_users(users):
    _write_json(USERS_FILE, [u.to_dict() for u in users.values()])


def load_products():
    return [Product.from_dict(entry) for entry in _read_json(PRODUCTS_FILE)]


def save_products(products):
    _write_json(PRODUCTS_FILE, [p.to_dict() for p in products])


def load_orders():
    return _read_json(ORDERS_FILE)


def save_order(order):
    orders = load_orders()
    orders.append(order)
    _write_json(ORDERS_FILE, orders)


def seed_default_data():
    from .utils import password

    users = load_users()
    if not users:
        admin = Admin("admin", password("admin123"))
        customer = Customer("john", password("john123"))
        save_users({admin.username: admin, customer.username: customer})

    if not load_products():
        save_products([
            Product("Wireless Mouse", 799, 25, "electronics"),
            Product("Notebook", 60, 100, "stationery"),
            Product("Bluetooth Speaker", 1999, 10, "electronics"),
            Product("Water Bottle", 249, 40, "lifestyle"),
        ])

