PRODUCTS = [
    {"id": "coffee", "name": "Coffee", "price": 60},
    {"id": "pizza", "name": "Pizza Slice", "price": 150},
    {"id": "sandwich", "name": "Sandwich", "price": 120},
    {"id": "juice", "name": "Juice", "price": 90},
]

DISCOUNTS = {"STUDENT10": 10, "TEACHER20": 20}

orders = []


def price_of(product_id):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product["price"]
    return 0


def cart_total(items):
    return sum(price_of(product_id) * qty for product_id, qty in items.items())


def apply_discount(total, code):
    percent = DISCOUNTS.get(code, 0)
    return total * (100 - percent) // 100


def pay(items, code=""):
    charged = apply_discount(cart_total(items), code)
    order = {"id": len(orders) + 1, "items": items, "code": code, "charged": charged}
    orders.append(order)
    return order


def reset():
    orders.clear()
