import random
import sqlite3
import time
from pathlib import Path

DB = Path(__file__).parent / "seats.db"

ROWS = ["A", "B", "C", "D"]
COLS = [1, 2, 3, 4, 5, 6]

PAYMENT_DELAY = (2, 4)  # the fake payment takes 2-4 seconds


def connect():
    return sqlite3.connect(DB)


def reset_db():
    with connect() as db:
        db.execute("DROP TABLE IF EXISTS seats")
        db.execute("CREATE TABLE seats (id TEXT PRIMARY KEY, booked_by TEXT)")
        for row in ROWS:
            for col in COLS:
                db.execute("INSERT INTO seats VALUES (?, NULL)", (f"{row}{col}",))


def all_seats():
    with connect() as db:
        rows = db.execute("SELECT id, booked_by FROM seats").fetchall()
    return [{"id": seat_id, "booked_by": booked_by} for seat_id, booked_by in rows]


def book_seat(seat_id, user):
    with connect() as db:
        taken = db.execute(
            "SELECT booked_by FROM seats WHERE id = ?", (seat_id,)
        ).fetchone()[0]
        if taken:
            return {"ok": False, "error": f"Seat {seat_id} is already booked by {taken}"}

        time.sleep(random.uniform(*PAYMENT_DELAY))  # processing payment...

        db.execute("UPDATE seats SET booked_by = ? WHERE id = ?", (user, seat_id))
    return {"ok": True, "seat": seat_id, "user": user}


def ticket(seat_id, user):
    with connect() as db:
        owner = db.execute(
            "SELECT booked_by FROM seats WHERE id = ?", (seat_id,)
        ).fetchone()[0]
    if owner == user:
        return {"ok": True, "seat": seat_id, "user": user}
    return {"ok": False, "error": f"Seat {seat_id} belongs to {owner}, not {user}!"}
