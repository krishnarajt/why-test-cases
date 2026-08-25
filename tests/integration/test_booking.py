# All the unit tests pass. They book seats ONE AT A TIME.
# But real life is not one at a time.
#
# Uncomment everything below, then run:
#   uv run pytest tests/integration/test_booking.py

# import threading

# from backend import booking


# def test_two_users_race_for_the_same_seat():
#     booking.reset_db()
#     results = []

#     def grab(user):
#         results.append(booking.book_seat("B3", user))

#     alice = threading.Thread(target=grab, args=("alice",))
#     bob = threading.Thread(target=grab, args=("bob",))
#     alice.start()
#     bob.start()
#     alice.join()
#     bob.join()

#     wins = [r for r in results if r["ok"]]
#     assert len(wins) == 1, f"Both users booked the same seat! {results}"
