# Problem Statement

**Project Title:** GreenCart — Online Store Login & Product Management System (CLI)

**Student Name:** _[your name]_
**Roll Number:** _[your roll number]_
**College / Course:** _[your college and course]_
**Submitted to:** _[teacher's name]_

## 1. Problem Statement
Online stores need a way to keep customer accounts secure while letting staff
manage the products being sold. This project builds a command-line application
that lets a user **register**, **log in**, and, depending on their role, either
**shop** (browse, search, add to cart, checkout) or **manage inventory**
(Create, Read, Update, Delete products). The goal is to apply core Python
concepts to a realistic, relatable problem instead of an abstract exercise.

## 2. Objectives
- Build a secure login/registration system (passwords hashed, never stored in plain text).
- Implement full CRUD operations on a product catalog.
- Separate users into two roles — **Customer** and **Admin** — with different permissions.
- Persist all data between runs using file storage (JSON), without needing a database server.
- Demonstrate Python fundamentals, OOP, and modular code organization in one working project.

## 3. Scope
**Included:**
- User registration and login with SHA-256 password hashing
- Role-based menus (Customer vs Admin)
- Product CRUD (Create, Read, Update, Delete) — Admin only
- Product search and category filtering
- Shopping cart, checkout, and order history — Customer only
- Low-stock report and top-products-by-value report — Admin only
- Data persistence via JSON files

**Not included (possible future work):**
- A graphical or web interface (this version is CLI-only by design)
- Real payment processing
- Multi-user concurrent access / a real database server

## 4. Tech Stack
- **Language:** Python 3 (standard library only — no external packages required)
- **Storage:** JSON files (`data/users.json`, `data/products.json`, `data/orders.json`)
- **Interface:** Command-line (text menus using `input()` / `print()`)

## 5. Core Python Concepts Applied
Python fundamentals, operators, precedence & associativity, input/output operations,
type conversion, core data structures (list, dict, tuple, set), control flow
(if/elif/else, for, while), functions, arrays, modules & packages, and
object-oriented programming (classes, inheritance, encapsulation, polymorphism).

## 6. System Design (brief)
- `main.py` — entry point; menu loop and user interaction
- `greencart/models.py` — `User`, `Customer`, `Admin`, `Product` classes (OOP)
- `greencart/storage.py` — reads/writes JSON files (persistence layer)
- `greencart/utils.py` — helper functions (hashing, calculations, validation)

## 7. Expected Outcome
A runnable CLI program where:
- A new customer can register, log in, browse/search products, add items to a
  cart, and complete a checkout that updates stock and saves an order.
- An admin can log in and perform full CRUD on the product catalog, plus view
  basic reports (low stock, top products, registered users).
- All data survives a restart of the program because it is saved to disk.

## 8. Future Enhancements
A delivery scheduler (using Python's `datetime` module), an SQLite-based storage
layer in place of JSON, discount coupons, and a password-change option.
