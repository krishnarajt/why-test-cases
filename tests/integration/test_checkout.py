# Uncomment everything below, then run:
#   uv run pytest tests/integration/test_checkout.py
#
# Unlike the others, these all PASS - the backend applies discounts correctly.
# So if a customer is still charged the wrong amount... where would you look?

# from fastapi.testclient import TestClient

# from backend.main import app

# client = TestClient(app)


# def test_preview_applies_discount():
#     client.post("/api/reset")
#     r = client.post("/api/preview", json={"items": {"coffee": 1, "pizza": 1}, "code": "STUDENT10"})
#     assert r.json() == {"total": 210, "after_discount": 189}


# def test_pay_applies_discount():
#     client.post("/api/reset")
#     r = client.post("/api/pay", json={"items": {"coffee": 1, "pizza": 1}, "code": "STUDENT10"})
#     assert r.json()["charged"] == 189


# def test_pay_without_code_charges_full_price():
#     client.post("/api/reset")
#     r = client.post("/api/pay", json={"items": {"coffee": 1, "pizza": 1}})
#     assert r.json()["charged"] == 210
