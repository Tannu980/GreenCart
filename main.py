

from datetime import datetime

from greencart import storage
from greencart.models import Customer, Product
from greencart.utils import (
    hash_password, verify_password, calculate_order_total, is_valid_order,
    to_safe_float, to_safe_int, format_price_for_display, categorize_products,
    find_low_stock_products, search_products_by_keyword, unique_categories,
    top_n_products_by_value,
)

MAX_LOGIN_ATTEMPTS = 3
LINE = "-" * 60



def ask(prompt):
    return input(prompt).strip()


def ask_password(prompt="Password: "):
    return input(prompt).strip()


def pause():
    input("\nPress Enter to continue...")


def heading(title):
    print(f"\n{LINE}\n  {title}\n{LINE}")




class GreenCartApp:

    def __init__(self):
        storage.seed_default_data()
        self.users = storage.load_users()          
        self.products = storage.load_products()    
        self.current_user = None



    def find_product(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def show_products(self, products):
        if not products:
            print("No products to show.")
            return
        print(f"{'ID':<5}{'Name':<24}{'Category':<14}{'Price':>10}{'Qty':>6}")
        print(LINE)
        for p in products:
            print(f"{p.id:<5}{p.name:<24}{p.category:<14}{p.price:>10.2f}{p.quantity:>6}")



    def register(self):
        heading("REGISTER")
        username = ask("Choose a username: ")
        if not username:
            print("Username cannot be empty.")
            return
        if username in self.users:
            print("That username is already taken.")
            return

        password = ask_password("Choose a password (min 6 characters): ")
        if len(password) < 6:
            print("Password is too short.")
            return
        if password != ask_password("Confirm password: "):
            print("Passwords do not match.")
            return

        self.users[username] = Customer(username, hash_password(password))
        storage.save_users(self.users)
        print("Account created! You can log in now.")

    def login(self):
        heading("LOGIN")
        attempts = 0
        while attempts < MAX_LOGIN_ATTEMPTS:          
            username = ask("Username: ")
            password = ask_password()
            user = self.users.get(username)

            if user is not None and verify_password(password, user.password):
                self.current_user = user
                print(f"\nWelcome, {user.username}! Logged in as {user.role}.")
                return True

            attempts += 1
            remaining = MAX_LOGIN_ATTEMPTS - attempts
            print(f"Invalid username or password. Attempts left: {remaining}")

        print("Too many failed attempts. Returning to main menu.")
        return False

    def logout(self):
        print(f"Goodbye, {self.current_user.username}!")
        self.current_user = None


    def search_products(self):
        keyword = ask("Enter keyword: ")
        self.show_products(search_products_by_keyword(self.products, keyword))

    def filter_by_category(self):
        print("Categories:", ", ".join(unique_categories(self.products)))
        category = ask("Enter category: ").lower()
        grouped = categorize_products(self.products)
        self.show_products(grouped.get(category, []))

    def add_to_cart(self):
        self.show_products(self.products)
        product = self.find_product(to_safe_int(ask("\nProduct ID to add: "), default=-1))
        if product is None:
            print("Product not found.")
            return
        quantity = to_safe_int(ask("Quantity: "))

        if not is_valid_order(quantity, product.quantity, self.current_user is not None):
            print(f"Invalid quantity. Available stock: {product.quantity}")
            return
        self.current_user.cart.append((product, quantity))    # tuple stored in list
        print(f"Added {quantity} x {product.name} to cart.")

    def view_cart(self):
        cart = self.current_user.cart
        if not cart:
            print("Your cart is empty.")
            return 0.0
        grand_total = 0.0
        for index, (product, quantity) in enumerate(cart, start=1):   # tuple unpacking
            line_total = calculate_order_total(product.price, quantity)
            grand_total += line_total
            print(f"{index}. {product.name} x {quantity} = {format_price_for_display(line_total)} (incl. 5% tax)")
        print(LINE)
        print(f"Cart total: {format_price_for_display(grand_total)}")
        return grand_total

    def checkout(self):
        total = self.view_cart()
        if total == 0:
            return
        if ask("Confirm order? (y/n): ").lower() != "y":
            print("Order cancelled.")
            return

        items = []
        for product, quantity in self.current_user.cart:
            product.quantity -= quantity               # reduce stock
            items.append({"product": product.name, "quantity": quantity})

        storage.save_products(self.products)
        storage.save_order({
            "user": self.current_user.username,
            "items": items,
            "total": round(total, 2),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        self.current_user.cart = []
        print("Order placed successfully. Thank you for shopping!")

    def order_history(self):
        my_orders = [o for o in storage.load_orders() if o["user"] == self.current_user.username]
        if not my_orders:
            print("You have no orders yet.")
            return
        for order in my_orders:
            names = ", ".join(f"{i['product']} x{i['quantity']}" for i in order["items"])
            print(f"{order['date']} | {names} | Rs. {order['total']}")

    def customer_menu(self):
        actions = {
            "1": ("View all products", lambda: self.show_products(self.products)),
            "2": ("Search products", self.search_products),
            "3": ("Filter by category", self.filter_by_category),
            "4": ("Add to cart", self.add_to_cart),
            "5": ("View cart", self.view_cart),
            "6": ("Checkout", self.checkout),
            "7": ("My order history", self.order_history),
            "8": ("Logout", None),
        }
        self.run_menu("CUSTOMER MENU", actions, exit_key="8")


    def create_product(self):                      
        name = ask("Product name: ")
        price = to_safe_float(ask("Price: "))
        quantity = to_safe_int(ask("Quantity: "), default=-1)
        category = ask("Category (default: general): ").lower() or "general"

        if not name or price <= 0 or quantity < 0:
            print("Invalid input. Product not created.")
            return
        product = Product(name, price, quantity, category)
        self.products.append(product)
        storage.save_products(self.products)
        print(f"Created: {product}")

    def update_product(self):                     
        self.show_products(self.products)
        product = self.find_product(to_safe_int(ask("\nProduct ID to update: "), default=-1))
        if product is None:
            print("Product not found.")
            return
        print("Leave a field blank to keep its current value.")
        new_name = ask(f"Name [{product.name}]: ")
        new_price = ask(f"Price [{product.price}]: ")
        new_qty = ask(f"Quantity [{product.quantity}]: ")
        new_category = ask(f"Category [{product.category}]: ")

        if new_name:
            product.name = new_name
        if new_price:
            product.price = to_safe_float(new_price, default=product.price)
        if new_qty:
            product.quantity = to_safe_int(new_qty, default=product.quantity)
        if new_category:
            product.category = new_category.lower()

        storage.save_products(self.products)
        print(f"Updated: {product}")

    def delete_product(self):                     
        self.show_products(self.products)
        product = self.find_product(to_safe_int(ask("\nProduct ID to delete: "), default=-1))
        if product is None:
            print("Product not found.")
            return
        if ask(f"Really delete '{product.name}'? (y/n): ").lower() == "y":
            self.products.remove(product)
            storage.save_products(self.products)
            print("Product deleted.")
        else:
            print("Deletion cancelled.")

    def low_stock_report(self):
        threshold = to_safe_int(ask("Show products with stock below (default 10): "), default=10)
        self.show_products(find_low_stock_products(self.products, threshold))

    def top_products(self):
        for rank, (name, value) in enumerate(top_n_products_by_value(self.products, 3), start=1):
            print(f"{rank}. {name}  -  stock value Rs. {value:.2f}")

    def list_users(self):
        for user in self.users.values():
            print(user)                            

    def admin_menu(self):
        actions = {
            "1": ("View all products (Read)", lambda: self.show_products(self.products)),
            "2": ("Add product (Create)", self.create_product),
            "3": ("Update product (Update)", self.update_product),
            "4": ("Delete product (Delete)", self.delete_product),
            "5": ("Low-stock report", self.low_stock_report),
            "6": ("Top products by stock value", self.top_products),
            "7": ("List all users", self.list_users),
            "8": ("Logout", None),
        }
        self.run_menu("ADMIN MENU", actions, exit_key="8")


    def run_menu(self, title, actions, exit_key):
        """Generic menu loop: shows options, runs the chosen function."""
        while True:
            heading(f"{title}  |  user: {self.current_user.username}")
            for key, (label, _) in actions.items():
                print(f"  {key}. {label}")
            choice = ask("\nChoose an option: ")

            if choice == exit_key:
                self.logout()
                return
            if choice in actions:
                print()
                actions[choice][1]()              
                pause()
            else:
                print("Invalid choice, please try again.")

    def start(self):
        while True:
            heading("WELCOME TO GREENCART")
            print("  1. Login\n  2. Register\n  3. Exit")
            choice = ask("\nChoose an option: ")

            if choice == "1":
                if self.login():
                    if self.current_user.role == "admin":
                        self.admin_menu()
                    else:
                        self.customer_menu()
            elif choice == "2":
                self.register()
                pause()
            elif choice == "3":
                print("Thanks for visiting GreenCart. Bye!")
                break
            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    try:
        GreenCartApp().start()
    except KeyboardInterrupt:
        print("\nExiting GreenCart. Bye!")
