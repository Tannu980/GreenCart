# GreenCart - Online Store Login System (CLI)

A beginner-friendly, command-line Python project: **login/register** for an online store
with **customer shopping** and **admin CRUD** on products. No external libraries needed.

## Run
```bash
python main.py
```
Demo accounts (created on first run): `admin` / `admin123` and `john` / `john123`.
Data is saved in the `data/` folder as JSON files.

## Structure
```
greencart_cli/
├── main.py               # menus + app flow (GreenCartApp class)
├── greencart/            # package
│   ├── __init__.py
│   ├── models.py         # OOP: User, Customer, Admin, Product
│   ├── storage.py        # file I/O with json, exception handling
│   └── utils.py          # hashing, operators, type conversion, loops, data structures
└── data/                 # auto-created: users.json, products.json, orders.json
```

## Syllabus topic -> where to find it
| Topic | Location |
|---|---|
| Python fundamentals | throughout `main.py` |
| Operators | `utils.py` -> `calculate_order_total()`, `is_valid_order()` |
| Precedence & associativity | comment block above `calculate_order_total()` in `utils.py` |
| Input / Output | `ask()`, `ask_password()`, `print()` in `main.py`; file I/O in `storage.py` |
| Type conversion | `to_safe_int()`, `to_safe_float()`, `format_price_for_display()` in `utils.py` |
| Data structures | list (`products`), dict (`users`, menu `actions`), tuple (cart items), set (`unique_categories`) |
| Control flow | `while` login attempts, `for` loops, `if/elif/else` menus |
| Functions | `utils.py` (default args, return values), lambdas in menu dicts |
| Arrays | `self.products` list, `Customer.cart` list |
| Modules & packages | `greencart/` package; imports of `json`, `os`, `hashlib`, `getpass`, `datetime` |
| OOP | `models.py`: inheritance, encapsulation, polymorphism, `@property`, `@classmethod` |
| CRUD | Admin menu: `create_product`, `show_products`, `update_product`, `delete_product` |

## Login flow (explain to your teacher)
1. User enters username and password (`getpass` hides the typing).
2. `verify_password()` hashes the typed password with SHA-256 and compares it with the stored hash.
   Plain-text passwords are never stored.
3. After 3 wrong attempts the user goes back to the main menu.
4. The user's `role` decides which menu opens: admin menu or customer menu.

## Likely viva questions
- **Why hash passwords?** So the stored file never reveals real passwords.
- **Where is inheritance used?** `Customer` and `Admin` extend `User` and override `describe()`.
- **Why `@property` on price?** Encapsulation: the setter rejects negative values.
- **How is data saved?** `storage.py` writes lists/dicts to JSON with the `json` module.

## Extension ideas
Delivery scheduler (`datetime`), SQLite instead of JSON, discount coupons, password change option,
sales report for admin.


