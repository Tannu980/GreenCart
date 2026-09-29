

import hashlib


def hash_password(plain_text_password):
    return hashlib.sha256(plain_text_password.encode("utf-8")).hexdigest()


def verify_password(plain_text_password, stored_hash):
    return hash_password(plain_text_password) == stored_hash



def calculate_order_total(price, quantity, tax_percent=5, discount_percent=0):
    subtotal = price * quantity
    discount_amount = subtotal * discount_percent / 100
    taxable_amount = subtotal - discount_amount
    tax_amount = taxable_amount * tax_percent / 100
    grand_total = taxable_amount + tax_amount
    return round(grand_total, 2)


def is_valid_order(quantity, stock_available, is_logged_in):
    return quantity > 0 and quantity <= stock_available and is_logged_in



def to_safe_float(value, default=0.0):
    try:
        return float(value)         
    except (TypeError, ValueError):
        return default


def to_safe_int(value, default=0):
    try:
        return int(float(value))   
    except (TypeError, ValueError):
        return default


def format_price_for_display(price):
    return "Rs. " + str(round(float(price), 2))




def categorize_products(products):
    grouped = {}                      
    for product in products:           
        if product.category in grouped:
            grouped[product.category].append(product)
        else:
            grouped[product.category] = [product]
    return grouped


def find_low_stock_products(products, threshold=5):
    return [p for p in products if p.quantity < threshold]


def search_products_by_keyword(products, keyword):
    results = []
    index = 0
    keyword_lower = keyword.lower()
    while index < len(products):
        product = products[index]
        if keyword_lower in product.name.lower():
            results.append(product)
        index += 1                   
    return results


def unique_categories(products):
    return sorted({p.category for p in products})  


def top_n_products_by_value(products, n=3):
    values = [(p.name, p.total_value()) for p in products]   
    values.sort(key=lambda item: item[1], reverse=True)
    return values[:n]




