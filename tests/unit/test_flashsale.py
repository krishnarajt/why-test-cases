# Run with:  uv run pytest tests/unit/test_flashsale.py
#
# Every test below passes. Buying works. Selling out works.
# None of them ever asked: what happens when 200 fans show up AT ONCE?
from backend import flashsale


def setup_function():
    flashsale.reset()


def test_buying_a_ticket_works(monkeypatch):
    monkeypatch.setattr(flashsale, "PAYMENT_DELAY", (0, 0))
    result = flashsale.buy("alice")
    assert result["ok"] is True
    assert result["left"] == flashsale.TICKETS - 1


def test_selling_out_is_handled(monkeypatch):
    monkeypatch.setattr(flashsale, "PAYMENT_DELAY", (0, 0))
    monkeypatch.setattr(flashsale, "tickets_left", 1)
    assert flashsale.buy("alice")["ok"] is True
    result = flashsale.buy("bob")
    assert result["ok"] is False
    assert "Sold out" in result["error"]
