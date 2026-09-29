# 🛒 GreenCart — Online Store Login & Product Management (CLI)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![Storage](https://img.shields.io/badge/storage-JSON-orange)
![Interface](https://img.shields.io/badge/interface-CLI-lightgrey)

A beginner-friendly, command-line Python project built as a college assignment.
It combines a **secure login/registration system** with **full CRUD** product
management for a small online store — all in pure Python, no external
libraries, no database server.

> Built to demonstrate Python fundamentals, OOP, and file-based persistence
> in one realistic, working application.

---

## 📑 Table of Contents

1. [Features](#-features)
2. [Tech Stack](#-tech-stack)
3. [System Architecture](#-system-architecture)
4. [Flow Diagrams](#-flow-diagrams)
5. [Data Model](#-data-model)
6. [Getting Started](#-getting-started)
7. [Usage Walkthrough](#-usage-walkthrough)
8. [Project Structure](#-project-structure)
9. [How Login Works](#-how-login-works)
10. [Python Concepts Covered](#-python-concepts-covered)
11. [Security Notes & Limitations](#-security-notes--limitations)
12. [Testing](#-testing)
13. [Troubleshooting](#-troubleshooting)
14. [Roadmap](#-roadmap--future-enhancements)
15. [Author](#-author)

---

## ✨ Features

**Everyone**
- Register a new account / log in (passwords hashed with SHA-256, never stored in plain text)
- 3 failed login attempts sends you back to the main menu
- Password input hidden while typing (`getpass`)

**Customers**
- Browse, search, and filter products by category
- Add items to a cart, check out, and view order history
- Stock is validated and updated automatically on checkout

**Admins**
- Full CRUD on the product catalog: Create, Read, Update, Delete
- Low-stock report and top-products-by-stock-value report
- View all registered users

---

## 🧰 Tech Stack

| Layer | Choice | Purpose |
|---|---|---|
| Language | Python 3.8+ | Core application logic |
| Interface | CLI (`input()` / `print()`) | Menu-driven user interaction |
| Storage | JSON files in `data/` | Lightweight file-based "database" |
| Security | `hashlib` (SHA-256), `getpass` | Password hashing and hidden input |
| Paradigm | Object-Oriented Programming | `User` → `Customer` / `Admin`, `Product` |
| Time | `datetime` | Order timestamps |
| Persistence | `json`, `os` | File I/O and directory handling |

**Standard-library modules used:** `json`, `os`, `hashlib`, `getpass`, `datetime`

No `pip install` needed — just Python itself.

---

## 🏛️ System Architecture

GreenCart follows a simple **layered structure**, separating menus, business
logic, and data persistence:

```mermaid
flowchart TB
    subgraph PRESENTATION["🖥️ main.py"]
        MAIN["GreenCartApp<br/>Menus & app flow"]
    end

    subgraph BUSINESS["⚙️ greencart package"]
        MODELS["models.py<br/>User · Customer · Admin · Product"]
        UTILS["utils.py<br/>Hashing · Validation · Calculations"]
    end

    subgraph DATA["💾 storage.py"]
        STORAGE["Read / Write JSON"]
    end

    subgraph FILES["📂 data/"]
        U[("users.json")]
        P[("products.json")]
        O[("orders.json")]
    end

    MAIN --> MODELS
    MAIN --> UTILS
    MAIN --> STORAGE
    STORAGE --> MODELS
    STORAGE --> U
    STORAGE --> P
    STORAGE --> O
```

### Layer responsibilities

| Layer | Module | Responsibility |
|---|---|---|
| Presentation | `main.py` | Displays menus, reads input, calls model/storage/utils functions |
| Business logic | `models.py` | Defines `User`, `Customer`, `Admin`, `Product` — data + small behaviors |
| Business logic | `utils.py` | Password hashing, safe type conversion, totals, validation, search/filter helpers |
| Data access | `storage.py` | Loads/saves JSON, handles a missing or corrupt file gracefully |

### Class diagram

Menus and login logic live in `main.py`, **not** on these classes — the
diagram below only shows what the classes themselves actually hold.

```mermaid
classDiagram
    class User {
        +int id
        -str password_hash
        +str username
        +str role
        +describe() str
        +to_dict() dict
    }
    class Customer {
        +list cart
        +describe() str
    }
    class Admin {
        +list permissions
        +describe() str
    }
    class Product {
        +int id
        +str name
        +str category
        -float price
        +int quantity
        +total_value() float
        +to_dict() dict
    }

    User <|-- Customer
    User <|-- Admin
```

`describe()` is overridden in each subclass — this is the project's example
of **polymorphism**. `password_hash` and `price` are private attributes
exposed only through `@property` — the project's example of **encapsulation**.

---

## 🔄 Flow Diagrams

### 1. Application flow (main menu → role menus)

```mermaid
flowchart TD
    START([python main.py]) --> INIT[Create data/ folder and seed demo accounts if missing]
    INIT --> MAIN{Main Menu}
    MAIN -->|1. Login| LOGIN[Login flow]
    MAIN -->|2. Register| REG[Register new customer]
    MAIN -->|3. Exit| END([Goodbye 👋])
    REG --> MAIN
    LOGIN --> ROLE{Role?}
    ROLE -->|customer| CUST[Customer Menu]
    ROLE -->|admin| ADM[Admin Menu]
    ROLE -->|failed 3x| MAIN
    CUST -->|Logout| MAIN
    ADM -->|Logout| MAIN
```

### 2. Login & authentication flow

```mermaid
flowchart TD
    A([Select Login]) --> B[attempts = 0]
    B --> C[/Enter username and password/]
    C --> D[Hash password with SHA-256]
    D --> E{User exists AND hash matches?}
    E -->|Yes| F[✅ Login successful]
    F --> G{role}
    G -->|admin| H[Admin Menu]
    G -->|customer| I[Customer Menu]
    E -->|No| J[attempts += 1]
    J --> K{attempts >= 3?}
    K -->|No| L[❌ Show error, try again]
    L --> C
    K -->|Yes| M[🔒 Too many attempts]
    M --> N([Return to Main Menu])
```

### 3. Customer shopping flow

```mermaid
flowchart TD
    C0([Customer Menu]) --> C1{Choose action}
    C1 --> B1[View all products]
    C1 --> B2[Search products]
    C1 --> B3[Filter by category]
    C1 --> B4[Add to cart]
    C1 --> B5[View cart]
    C1 --> B6[Checkout]
    C1 --> B7[Order history]
    C1 --> B8([Logout])

    B4 --> V1{Quantity valid and in stock?}
    V1 -->|Yes| B4A[Add id, quantity tuple to cart]
    V1 -->|No| B4B[Show invalid quantity message]

    B6 --> V2{Cart total > 0?}
    V2 -->|No| B6A[Show empty-cart message]
    V2 -->|Yes| B6B[Confirm with user? y/n]
    B6B -->|y| B6C[Reduce stock, save order, clear cart]
    B6B -->|n| B6D[Order cancelled]
```

### 4. Checkout sequence

```mermaid
sequenceDiagram
    actor C as Customer
    participant M as main.py
    participant U as utils.py
    participant S as storage.py
    participant F as data/*.json

    C->>M: Select "Checkout"
    M->>M: Loop through cart tuples (product, quantity)
    M->>U: calculate_order_total(price, quantity) per item
    U-->>M: line total (with tax)
    M->>M: Reduce product.quantity for each item
    M->>S: save_products(products)
    S->>F: write products.json
    M->>S: save_order({user, items, total, date})
    S->>F: append to orders.json
    M-->>C: "Order placed successfully"
```

### 5. Admin CRUD flow

```mermaid
flowchart LR
    ADM([Admin Menu]) --> CRUD{Manage Products}
    CRUD -->|Create| CR[Add new product]
    CRUD -->|Read| RD[View all products]
    CRUD -->|Update| UP[Edit name, price, quantity, category]
    CRUD -->|Delete| DL[Remove product, with confirm]
    ADM --> RPT{Reports}
    RPT --> LS[Low-stock report]
    RPT --> TP[Top products by stock value]
    ADM --> VU[List all users]
    CR & UP & DL --> SAVE[(Save to products.json)]
```

---

## 🗄️ Data Model

GreenCart stores data as flat JSON **lists of records** (not a relational
database) — one file per entity:

```mermaid
flowchart LR
    subgraph users.json
        U1["id, username,<br/>password_hash, role"]
    end
    subgraph products.json
        P1["id, name, category,<br/>price, quantity"]
    end
    subgraph orders.json
        O1["user, items[ ],<br/>total, date"]
        O2["each item: product, quantity"]
    end
```

### Real record shapes (from `storage.py` / `models.py`)

**`data/users.json`** — a list, keyed by nothing (username is a field):
```json
[
  { "id": 1, "username": "admin", "password_hash": "<sha256-hex>", "role": "admin" },
  { "id": 2, "username": "john",  "password_hash": "<sha256-hex>", "role": "customer" }
]
```

**`data/products.json`**:
```json
[
  { "id": 1, "name": "Wireless Mouse", "price": 799.0, "quantity": 25, "category": "electronics" }
]
```

**`data/orders.json`**:
```json
[
  {
    "user": "john",
    "items": [ { "product": "Wireless Mouse", "quantity": 2 } ],
    "total": 1677.9,
    "date": "2026-09-28 07:47"
  }
]
```

---

## 🚀 Getting Started

### Prerequisites
- Python **3.8 or newer** (check with `python --version`)
- Git (optional, for cloning)

### Installation & run

```bash
git clone https://github.com/<your-username>/greencart-cli.git
cd greencart-cli
python main.py
```

> On some systems use `python3 main.py` instead.

**Demo accounts** (auto-created on first run):

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Customer | `john` | `john123` |

Or register your own account from the main menu.

> ⚠️ These demo credentials are for local testing only. Change or remove them before any real use.

---

## 🎮 Usage Walkthrough

```text
------------------------------------------------------------
  WELCOME TO GREENCART
------------------------------------------------------------
  1. Login
  2. Register
  3. Exit

Choose an option: 2
Username: john
Password: ********
Welcome back, john! Logged in as customer.

------------------------------------------------------------
  CUSTOMER MENU  |  user: john
------------------------------------------------------------
  1. View all products
  2. Search products
  3. Filter by category
  4. Add to cart
  5. View cart
  6. Checkout
  7. My order history
  8. Logout
```

> Replace this sample with a real screenshot or terminal recording of your app.

---

## 📁 Project Structure

```
greencart_cli/
├── main.py               # Entry point — menus and app flow (GreenCartApp)
├── greencart/
│   ├── __init__.py
│   ├── models.py          # OOP: User, Customer, Admin, Product
│   ├── storage.py         # File I/O — reads/writes JSON "database"
│   └── utils.py           # Hashing, calculations, validation, helpers
├── data/                  # Auto-created on first run (ignored by git)
│   ├── users.json
│   ├── products.json
│   └── orders.json
├── statement.md            # Problem statement / project brief
├── .gitignore
└── README.md
```

---

## 🔐 How Login Works

1. You enter a username and password (hidden while typing via `getpass`).
2. `utils.verify_password()` hashes the typed password with **SHA-256** and
   compares it to the stored hash — the real password is never saved anywhere.
3. On success, your `role` (`customer` or `admin`) decides which menu you get.
4. Three wrong attempts in a row sends you back to the main menu.

See the [login flow diagram](#2-login--authentication-flow) above.

---

## 🧠 Python Concepts Covered

| Concept | Where |
|---|---|
| Operators, precedence & associativity | `utils.py` → `calculate_order_total()` |
| Type conversion | `utils.py` → `to_safe_int()`, `to_safe_float()` |
| Data structures (list, dict, tuple, set) | products list, users dict, cart tuples, `unique_categories()` |
| Control flow (`if`/`elif`/`while`/`for`) | login attempt loop, menu loops in `main.py` |
| Functions (default & keyword args) | throughout `utils.py` |
| Modules & packages | `greencart/` package; `json`, `os`, `hashlib`, `getpass`, `datetime` |
| OOP (inheritance, encapsulation, polymorphism) | `models.py` → `User` → `Customer` / `Admin` |
| File I/O & exception handling | `storage.py` |
| CRUD | Admin menu in `main.py` |

---

## 🛡️ Security Notes & Limitations

This is a **learning project**, not production software. Known limitations:

| Area | Current state | Better practice |
|---|---|---|
| Password hashing | Plain SHA-256 (fast, unsalted) | Use a salted, slow KDF such as `hashlib.pbkdf2_hmac`, `bcrypt`, or `argon2` |
| Storage | Unencrypted JSON files | Use a real database with access control |
| Lockout | Resets whenever you return to the main menu | Persist attempts and add a timed lockout |
| Concurrency | No file locking; not safe for multiple users at once | Use a database or file locks |
| Demo accounts | Hard-coded credentials | Remove or force a password change on first login |

Good things already in place: no plain-text passwords, hidden password input,
input validation, and role-based menu access.

---

## 🧪 Testing

There's no automated test suite yet — testing is manual. Suggested checklist:

- [ ] Register a new user, then log in with it
- [ ] Log in with a wrong password 3 times → returned to main menu
- [ ] Register with an existing username → rejected
- [ ] Customer: try to add more of an item than is in stock → rejected
- [ ] Customer: checkout reduces stock and creates an order
- [ ] Admin: create, update, and delete a product
- [ ] Admin: low-stock report shows the expected items
- [ ] Enter letters where a number is expected → no crash
- [ ] Delete the `data/` folder and restart → demo data is recreated

Adding automated tests with Python's built-in `unittest` module is listed
under [Roadmap](#-roadmap--future-enhancements).

---

## 🩺 Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found` | Use `python3`, or install Python from [python.org](https://www.python.org/downloads/) |
| `ModuleNotFoundError: No module named 'greencart'` | Run `python main.py` from the project's root folder, not from inside `greencart/` |
| Password not visible while typing | Expected — `getpass` hides input. In some IDE consoles it may not work, so use a real terminal |
| App crashes or data looks corrupted on start | Delete the `data/` folder; it is recreated with demo data on the next run |
| Forgot the admin password | Delete `data/users.json` to reset to the demo accounts |

---

## 🗺️ Roadmap / Future Enhancements

- [ ] Delivery scheduler using `datetime`
- [ ] Swap JSON storage for SQLite
- [ ] Discount coupons
- [ ] Change-password option
- [ ] Salted password hashing (PBKDF2 / bcrypt)
- [ ] Automated unit tests with `unittest`
- [ ] Export orders to CSV

---

## 👤 Author

**[Your Name]** — [your.email@example.com]
Built as a college Python project, [Month Year].



