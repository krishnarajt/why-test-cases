# Run with:  uv run pytest tests/unit/test_booking.py
from backend import booking


def setup_function():
    booking.PAYMENT_DELAY = (0, 0)  # skip the fake payment wait in tests
    booking.reset_db()


def test_all_seats_start_free():
    assert all(seat["booked_by"] is None for seat in booking.all_seats())


def test_booking_a_free_seat():
    result = booking.book_seat("B3", "alice")
    assert result["ok"] is True


def test_booking_a_taken_seat_fails():
    booking.book_seat("B3", "alice")
    result = booking.book_seat("B3", "bob")
    assert result["ok"] is False


def test_ticket_belongs_to_the_booker():
    booking.book_seat("B3", "alice")
    assert booking.ticket("B3", "alice")["ok"] is True
    assert booking.ticket("B3", "bob")["ok"] is False
