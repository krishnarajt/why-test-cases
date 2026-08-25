# Run with:  uv run pytest tests/unit/test_users.py
from backend import users


def setup_function():
    users.reset_db()


def test_good_username():
    assert users.valid_username("alice") is True


def test_bad_username():
    assert users.valid_username("a") is False


def test_good_password():
    assert users.valid_password("1234") is True


def test_short_password():
    assert users.valid_password("123") is False


def test_signup_then_login():
    assert users.signup("alice", "1234")["ok"] is True
    assert users.login("alice", "1234")["ok"] is True


def test_wrong_password():
    users.signup("alice", "1234")
    assert users.login("alice", "9999")["ok"] is False
