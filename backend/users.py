import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "users.db"


def connect():
    return sqlite3.connect(DB)


def reset_db():
    with connect() as db:
        db.execute("DROP TABLE IF EXISTS users")
        db.execute("CREATE TABLE users (username TEXT UNIQUE, password TEXT)")


def valid_username(username):
    return username.isalnum() and 3 <= len(username) <= 20


def valid_password(password):
    return len(password) >= 4


def signup(username, password):
    if not valid_username(username):
        return {"ok": False, "error": "Username must be 3-20 letters or numbers"}
    if not valid_password(password):
        return {"ok": False, "error": "Password must be at least 4 characters"}
    with connect() as db:
        db.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    return {"ok": True, "user": username}


def login(username, password):
    with connect() as db:
        row = db.execute(
            "SELECT password FROM users WHERE username = ?", (username,)
        ).fetchone()
    if row and row[0] == password:
        return {"ok": True, "user": username}
    return {"ok": False, "error": "Wrong username or password"}
