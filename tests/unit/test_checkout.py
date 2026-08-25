# Run with:  uv run pytest tests/unit/test_checkout.py
from backend import checkout


def setup_function():
    checkout.reset()


def test_cart_total():
    assert checkout.cart_total({"coffee": 2}) == 120


def test_discount_code_works():
    assert checkout.apply_discount(200, "STUDENT10") == 180


def test_unknown_code_changes_nothing():
    assert checkout.apply_discount(200, "FREESTUFF") == 200


def test_pay_charges_the_discounted_total():
    order = checkout.pay({"pizza": 1}, "STUDENT10")
    assert order["charged"] == 135
