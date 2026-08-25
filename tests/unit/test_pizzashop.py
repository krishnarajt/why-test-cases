# Run with:  uv run pytest tests/unit/test_pizzashop.py
#
# Every test below passes. The v1 flows were tested when v1 shipped.
# The new combo feature was tested when v2 shipped.
# So if the shop is quietly losing money... which flow did nobody RE-test?
from backend import pizzashop


def setup_function():
    pizzashop.reset()


# ---- written when v1 shipped ----

def test_single_item_cart():
    assert pizzashop.cart_total({"juice": 1}) == 90


def test_plain_cart():
    assert pizzashop.cart_total({"pizza": 1, "garlic": 1}) == 230


def test_pay_charges_the_total():
    order = pizzashop.pay({"brownie": 2})
    assert order["charged"] == 220


# ---- written when v2 shipped ----

def test_combo_prices_pizza_plus_juice_at_199():
    pizzashop.ship(2)
    assert pizzashop.cart_total({"pizza": 1, "juice": 1}) == 199


def test_two_combos():
    pizzashop.ship(2)
    assert pizzashop.cart_total({"pizza": 2, "juice": 2}) == 398


def test_combo_plus_a_brownie():
    pizzashop.ship(2)
    assert pizzashop.cart_total({"pizza": 1, "juice": 1, "brownie": 1}) == 309
