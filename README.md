# 🛒 GreenCart — Online Store Login & Product Management (CLI)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![Storage](https://img.shields.io/badge/storage-JSON-orange)
![Interface](https://img.shields.io/badge/interface-CLI-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

A beginner-friendly, command-line Python project built as a college assignment.
It combines a **secure login/registration system** with **full CRUD** product
management for a small online store, all in pure Python: no external
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
15. [Contributing](#-contributing)
16. [License](#-license)
17. [Author](#-author)

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
| Version Control | Git & GitHub | Source management |

**Standard-library modules used:** `json`, `os`, `hashlib`, `getpass`, `datetime`

No `pip install` needed, just Python itself.

---

## 🏛️ System Architecture

GreenCart follows a simple **layered architecture**, separating the user
interface, business logic, and data persistence so each part can change
independently (e.g., swapping JSON for SQLite later).

```mermaid
flowchart TB
    subgraph PRESENTATION["🖥️ Presentation Layer"]
        MAIN["main.py<br/>Menus & app flow"]
    end

    subgraph BUSINESS["⚙️ Business Logic Layer"]
        MODELS["models.py<br/>User · Customer · Admin · Product"]
        UTILS["utils.py<br/>Hashing · Validation · Calculations"]
    end

    subgraph DATA["💾 Data Access Layer"]
        STORAGE["storage.py<br/>Read / Write JSON"]
    end

    subgraph FILES["📂 Persistent Storage (data/)"]
        U[("users.json")]
        P[("products.json")]
        O[("orders.json")]
    end

    MAIN --> MODELS
    MAIN --> UTILS
    MAIN --> STORAGE
    MODELS --> UTILS
    STORAGE --> U
    STORAGE --> P
    STORAGE --> O
```

### Layer responsibilities

| Layer | Module | Responsibility |
|---|---|---|
| Presentation | `main.py` | Displays menus, reads input, routes to the right role menu |
| Business logic | `models.py` | Defines entities and role-specific behavior (polymorphism) |
| Business logic | `utils.py` | Password hashing, safe type conversion, totals, validation |
| Data access | `storage.py` | Loads/saves JSON, handles missing/corrupt files gracefully |

### Class diagram

```mermaid
classDiagram
    class User {
        -str username
        -str _password_hash
        +str role
        +check_password(password) bool
        +menu()* void
        +to_dict() dict
    }
    class Customer {
        +list cart
        +add_to_cart(product, qty) void
        +checkout() Order
        +menu() void
    }
    class Admin {
        +add_product() void
        +update_product() void
        +delete_product() void
        +view_reports() void
        +menu() void
    }
    class Product {
        +int id
        +str name
        +str category
        +float price
        +int stock
        +to_dict() dict
    }

    User <|-- Customer
    User <|-- Admin
    Customer "1" --> "*" Product : cart contains
    Admin "1" --> "*" Product : manages
```

---

## 🔄 Flow Diagrams

### 1. Application flow (main menu → role menus)

```mermaid
flowchart TD
    START([python main.py]) --> INIT[Create data/ folder and seed demo accounts if missing]
    INIT --> MAIN{Main Menu}
    MAIN -->|1. Register| REG[Register new customer]
    MAIN -->|2. Login| LOGIN[Login flow]
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
    C1 --> B1[Browse all products]
    C1 --> B2[Search by name]
    C1 --> B3[Filter by category]
    C1 --> B4[Add to cart]
    C1 --> B5[View cart]
    C1 --> B6[Checkout]
    C1 --> B7[Order history]
    C1 --> B8([Logout])

    B4 --> V1{Stock available?}
    V1 -->|Yes| B4A[Add item to cart]
    V1 -->|No| B4B[Show out-of-stock message]

    B6 --> V2{Cart empty?}
    V2 -->|Yes| B6A[Show empty-cart message]
    V2 -->|No| B6B[Re-validate stock]
    B6B -->|OK| B6C[Reduce stock, save order, clear cart]
    B6B -->|Insufficient| B6D[Report problem item]
```

### 4. Checkout sequence

```mermaid
sequenceDiagram
    actor C as Customer
    participant M as main.py
    participant U as utils.py
    participant S as storage.py
    participant F as JSON files

    C->>M: Select "Checkout"
    M->>S: load_products()
    S->>F: read products.json
    F-->>S: product data
    S-->>M: products
    M->>M: Validate stock for each cart item
    M->>U: calculate_order_total(cart)
    U-->>M: total
    M->>S: save_products(updated stock)
    S->>F: write products.json
    M->>S: save_order(order)
    S->>F: write orders.json
    M-->>C: Order confirmation + total
```

### 5. Admin CRUD flow

```mermaid
flowchart LR
    ADM([Admin Menu]) --> CRUD{Manage Products}
    CRUD -->|Create| CR[Add new product]
    CRUD -->|Read| RD[List / view products]
    CRUD -->|Update| UP[Edit price, stock, name...]
    CRUD -->|Delete| DL[Remove product]
    ADM --> RPT{Reports}
    RPT --> LS[Low-stock report]
    RPT --> TP[Top products by stock value]
    ADM --> VU[View all users]
    CR & UP & DL --> SAVE[(Save to products.json)]
```

---

## 🗄️ Data Model

Entity–relationship view of the JSON "database":

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : "appears in"

    USER {
        string username PK
        string password_hash
        string role "customer | admin"
    }
    PRODUCT {
        int id PK
        string name
        string category
        float price
        int stock
    }
    ORDER {
        int order_id PK
        string username FK
        string timestamp
        float total
    }
    ORDER_ITEM {
        int product_id FK
        int quantity
        float unit_price
    }
```

### Example records

**`data/users.json`**
```json
{
  "admin": { "password_hash": "<sha256-hex>", "role": "admin" },
  "john":  { "password_hash": "<sha256-hex>", "role": "customer" }
}
```

**`data/products.json`**
```json
[
  { "id": 1, "name": "Bamboo Toothbrush", "category": "Personal Care", "price": 2.99, "stock": 50 }
]
```

**`data/orders.json`**
```json
[
  {
    "order_id": 1,
    "username": "john",
    "timestamp": "2025-01-15 14:32:10",
    "items": [ { "product_id": 1, "quantity": 2, "unit_price": 2.99 } ],
    "total": 5.98
  }
]
```

> The exact field names may differ slightly. See `storage.py` and `models.py` for the source of truth.

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
=== Welcome to GreenCart ===
1. Register
2. Login
3. Exit
Choose an option: 2
Username: john
Password: ********
✅ Welcome back, john!

--- Customer Menu ---
1. Browse products
2. Search products
3. Filter by category
4. Add to cart
5. View cart
6. Checkout
7. Order history
8. Logout
```

> Replace this sample with a real screenshot or terminal recording of your app (e.g., using [asciinema](https://asciinema.org/)).

---

## 📁 Project Structure

```
greencart_cli/
├── main.py               # Entry point: menus and app flow
├── greencart/
│   ├── __init__.py
│   ├── models.py         # OOP: User, Customer, Admin, Product
│   ├── storage.py        # File I/O: reads/writes JSON "database"
│   └── utils.py          # Hashing, calculations, validation, helpers
├── data/                 # Auto-created on first run (ignored by git)
│   ├── users.json
│   ├── products.json
│   └── orders.json
├── statement.md          # Problem statement / project brief
├── .gitignore
└── README.md
```

---

## 🔐 How Login Works

1. You enter a username and password (hidden while typing via `getpass`).
2. The password is hashed with **SHA-256** and compared against the stored hash;
   the real password is never saved anywhere.
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
| Lockout | Resets when you return to the menu | Persist attempts and add a timed lockout |
| Concurrency | No file locking | Use a database or file locks for multi-user access |
| Demo accounts | Hard-coded credentials | Remove or force a password change on first login |

Good things already in place: no plain-text passwords, hidden password input,
input validation, and role-based menu access.

---

## 🧪 Testing

Manual test checklist:

- [ ] Register a new user, then log in with it
- [ ] Log in with a wrong password 3 times → returned to main menu
- [ ] Register with an existing username → rejected
- [ ] Customer: add item beyond available stock → rejected
- [ ] Customer: checkout reduces stock and creates an order
- [ ] Admin: create, update, and delete a product
- [ ] Admin: low-stock report shows expected items
- [ ] Enter letters where a number is expected → no crash
- [ ] Delete `data/` and restart → demo data is recreated

*Optional next step:* add automated tests with the built-in `unittest` module:

```bash
python -m unittest discover tests
```

---

## 🩺 Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found` | Use `python3`, or install Python from [python.org](https://www.python.org/downloads/) |
| `ModuleNotFoundError: greencart` | Run `python main.py` from the project's root folder |
| Password not visible while typing | Expected: `getpass` hides input. In some IDE consoles it may not work, so use a real terminal |
| Data looks corrupted / app crashes on start | Delete the `data/` folder; it is recreated with demo data on next run |
| Forgot admin password | Delete `data/users.json` to reset to the demo accounts |

---

## 🗺️ Roadmap / Future Enhancements

- [ ] Delivery scheduler using `datetime`
- [ ] Swap JSON storage for SQLite
- [ ] Discount coupons
- [ ] Change-password option
- [ ] Salted password hashing (PBKDF2 / bcrypt)
- [ ] Automated unit tests
- [ ] Export orders to CSV
- [ ] Simple GUI or web front end (Tkinter / Flask)

---

## 🤝 Contributing

Suggestions and improvements are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for details.

---

## 👤 Author

**[Your Name]** — [your.email@example.com]
GitHub: [@your-username](https://github.com/your-username)

Built as a college Python project, [Month Year].



