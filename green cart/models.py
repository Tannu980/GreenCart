
class User:

    _next_id = 1          

    def _init_(self, username, password, role="customer"):
        self.id = User._next_id
        User._next_id += 1
        self.username = username
        self._password = password    
        self.role = role

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_hash):
        if not new_hash:
            raise ValueError("Password cannot be empty")
        self._password = new_hash

    def describe(self):
        return f"User #{self.id} ({self.username}) - role: {self.role}"

    def to_dict(self):
        return {"id": self.id, "username": self.username,
                "password": self._password, "role": self.role}

    def _restore_id(self, saved_id, previous_next):
        self.id = saved_id
        User._next_id = max(previous_next, saved_id + 1)

    def _str_(self):
        return self.describe()

    def _repr_(self):
        return f"User(id={self.id}, username={self.username!r})"


class Customer(User):

    def _init_(self, username, password):
        super()._init_(username, password, role="customer")
        self.cart = []                  

    def describe(self):                 
        return f"Customer #{self.id} ({self.username}) - items in cart: {len(self.cart)}"

    @classmethod
    def from_dict(cls, data):
        before = User._next_id
        customer = cls(data["username"], data["password"])
        customer._restore_id(data["id"], before)
        return customer


class Admin(User):

    def _init_(self, username, password):
        super()._init_(username, password, role="admin")
        self.permissions = ["create", "read", "update", "delete"]

    def describe(self):                 # polymorphism
        return f"Admin #{self.id} ({self.username}) - permissions: {', '.join(self.permissions)}"

    @classmethod
    def from_dict(cls, data):
        before = User._next_id
        admin = cls(data["username"], data["password"])
        admin._restore_id(data["id"], before)
        return admin


class Product:

    _next_id = 1

    def _init_(self, name, price, quantity, category="general"):
        self.id = Product._next_id
        Product._next_id += 1
        self.name = name
        self._price = float(price)         
        self.quantity = int(quantity)
        self.category = category

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    def total_value(self):
        """Stock value = price * quantity."""
        return self._price * self.quantity

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self._price,
                "quantity": self.quantity, "category": self.category}

    @classmethod
    def from_dict(cls, data):
        before = cls._next_id
        product = cls(data["name"], data["price"], data["quantity"], data.get("category", "general"))
        product.id = data["id"]
        cls._next_id = max(before, data["id"] + 1)
        return product

    def _str_(self):
        return f"{self.name} - Rs.{self._price:.2f} x {self.quantity} ({self.category})"
