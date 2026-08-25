# All the unit tests pass. But they only ever sign up a username ONCE.
# What happens when a second person picks the same username?
#
# Uncomment everything below, then run:
#   uv run pytest tests/integration/test_users.py

# from fastapi.testclient import TestClient
#
# from backend.main import app
#
# client = TestClient(app)
#
#
# def test_signing_up_twice_gets_a_polite_error():
#     client.post("/api/reset")
#
#     first = client.post("/api/signup", json={"username": "alice", "password": "1234"})
#     assert first.json()["ok"] is True
#
#     second = client.post("/api/signup", json={"username": "alice", "password": "1234"})
#     assert second.json()["ok"] is False
#     assert "taken" in second.json()["error"]
