import inspect

PRODUCTS = [
    {"id": "pizza", "name": "Pizza Slice", "price": 150},
    {"id": "juice", "name": "Juice", "price": 90},
    {"id": "garlic", "name": "Garlic Bread", "price": 80},
    {"id": "brownie", "name": "Brownie", "price": 110},
]

COMBO_PRICE = 199  # v2's new Lunch Combo: 1 pizza + 1 juice

version = 1
orders = []


def price_of(product_id):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product["price"]
    return 0


def cart_total_v1(items):
    """The original pricing function. Boring. Correct. In production for months."""
    total = 0
    for product_id, qty in items.items():
        total += price_of(product_id) * qty
    return total


def cart_total_v2(items):
    """v2: every Pizza + Juice pair now rings up as one Lunch Combo."""
    combos = min(items.get("pizza", 0), items.get("juice", 0))
    total = combos * COMBO_PRICE
    for product_id, qty in items.items():
        if product_id in ("pizza", "juice"):
            continue  # combo items were already priced above
        total += price_of(product_id) * qty
    return total


def cart_total(items):
    return cart_total_v2(items) if version == 2 else cart_total_v1(items)


def ship(new_version):
    global version
    version = 2 if new_version == 2 else 1
    return version


def pay(items):
    charged = cart_total(items)
    order = {"id": len(orders) + 1, "items": items, "charged": charged, "version": version}
    orders.append(order)
    return order


def source_code():
    return {
        "v1": inspect.getsource(cart_total_v1),
        "v2": inspect.getsource(cart_total_v2),
        "active": version,
    }


def reset():
    global version
    version = 1
    orders.clear()
