# SPOILERS — the intentional bugs and their fixes

This file is for the instructor and for AI coding agents asked to "fix the bug"
or "write the tests". **Keep it off the projector — the audience should guess.**

Every bug here is intentional. When fixing one, change ONLY what's needed —
the rest of the code is deliberately simple and should stay that way.

Demos 5 and 6 ship **no fix, on purpose** — their lesson is a practice
(a manual regression pass; a load test), not a patch. If asked to "fix" them,
don't: the demo depends on the bug staying in.

---

## 1. Calculator — subtract is reversed

- **Bug:** `backend/calculator.py` → `subtract(a, b)` returns `b - a` instead of `a - b`.
  On the UI, `10 − 4` shows `-6`.
- **Tests:** `tests/unit/test_calculator.py` is fully commented out. Uncommenting it
  and running `uv run pytest tests/unit/test_calculator.py` makes `test_subtract` fail.
- **Fix:** return `a - b`.
- **Lesson:** even trivial code deserves a unit test.

## 2. Movie seats — check-then-sleep-then-write race condition

- **Bug:** `backend/booking.py` → `book_seat()` SELECTs the seat, then sleeps 2–4s
  (fake payment), then UPDATEs. Two users clicking the same seat within the sleep
  window both pass the "is it free?" check and both get `ok: True`. The last write
  wins the seat; the other user's ticket check fails.
- **Tests:** unit tests pass (they book sequentially). The commented-out
  integration test in `tests/integration/test_booking.py` books the same seat from
  two threads and fails: both threads succeed.
- **Fix:** make the claim atomic — replace the SELECT + UPDATE with a single
  conditional write and check `rowcount`:

  ```python
  def book_seat(seat_id, user):
      time.sleep(random.uniform(*PAYMENT_DELAY))  # processing payment...
      with connect() as db:
          claimed = db.execute(
              "UPDATE seats SET booked_by = ? WHERE id = ? AND booked_by IS NULL",
              (user, seat_id),
          )
          if claimed.rowcount == 0:
              return {"ok": False, "error": f"Seat {seat_id} is already booked"}
      return {"ok": True, "seat": seat_id, "user": user}
  ```

  Keep the sleep (the demo needs the payment delay) — just make sure the
  check-and-claim happens atomically. Keep `PAYMENT_DELAY` patchable so unit
  tests stay fast.
- **Lesson:** concurrency bugs never show up in one-at-a-time unit tests.

## 3. Login — unhandled UNIQUE constraint → 500

- **Bug:** `backend/users.py` → the `users` table declares `username TEXT UNIQUE`,
  but `signup()` INSERTs blindly. A second signup with the same username raises
  `sqlite3.IntegrityError`, which FastAPI turns into a 500 Internal Server Error.
- **Tests:** unit tests pass (they never sign up the same name twice). The
  commented-out integration test in `tests/integration/test_users.py` signs up
  "alice" twice through the API and expects `{"ok": false, "error": "...taken..."}` —
  instead the request explodes with IntegrityError.
- **Fix:** handle the duplicate and return a friendly error (the test expects the
  word "taken" in it):

  ```python
  try:
      with connect() as db:
          db.execute("INSERT INTO users VALUES (?, ?)", (username, password))
  except sqlite3.IntegrityError:
      return {"ok": False, "error": "That username is already taken"}
  ```
- **Lesson:** DB constraints only fire against the real DB — that's what
  integration tests are for.

## 4. Snack shop — frontend forgets to send the discount code

- **Bug:** `frontend/index.html` → the Pay button's handler calls
  `api("/api/pay", { items: cart })` **without the `code` field**. The UI shows the
  discounted total, but the backend (correctly) charges full price for a payload
  with no code. The receipt shows more than the button promised.
- **Tests:** ALL backend tests pass — unit AND integration (the integration file
  is commented out like the others, but passes once enabled) — because the
  backend really is correct. This bug is only visible by clicking through the UI.
- **Fix:** in the `payBtn` onclick handler, send the applied code:

  ```js
  const code = discounted !== null ? document.getElementById("codeInput").value.toUpperCase() : "";
  const order = await (await api("/api/pay", { items: cart, code })).json();
  ```
- **Lesson:** green test suites don't cover what nobody tests — always do a
  manual test run of the real flow.

## 5. Pizza shop v2 — the combo refactor makes old carts (nearly) free

- **Bug:** `backend/pizzashop.py` → the v2 "Lunch Combo" refactor of the pricing
  function. `cart_total_v2()` prices the pizza+juice combos first, then loops the
  cart and `continue`s past **every** pizza/juice line, assuming they were all
  consumed by combos. Any pizza or juice *not* part of a combo is never charged:
  a lone juice rings up ₹0, and 2 pizzas + 1 juice charges ₹199 instead of ₹349.
  It's a pure **undercharge** — no customer will ever report it; the shop just
  quietly loses money.
- **Demo mechanics:** the version flag flips at runtime via the tab's
  **🚀 Ship v2** button (`POST /api/pizzashop/ship`). The tab shows the shipped
  function's real source (`inspect.getsource` via `GET /api/pizzashop/code`) so
  the audience can find the bug on screen. Reset returns to v1.
- **Tests:** `tests/unit/test_pizzashop.py` — **all pass.** The v1 flows were
  tested against v1, the new combo is tested against v2. No test re-runs the old
  flows on the new code; that gap is the whole point.
- **Fix:** none shipped, by design. The lesson is the practice: a **manual
  regression pass** — re-test every flow that already worked whenever shared
  code changes (the tab's release checklist is that pass, made visible).
- **Lesson:** the new feature working proves nothing about the old flows —
  regressions live in the code you didn't re-test. Undercharges are the worst
  kind: nobody complains, so only re-testing catches them.

## 6. Flash sale — works for one fan, melts for 200

- **Bug:** there is no line to point at — that's the point. Every purchase in
  `backend/flashsale.py` sleeps 1.5–3 s ("payment"), `/api/flashsale/buy` is a
  sync endpoint, and the server has ~40 worker threads. One fan: ~2 s. 200 fans
  at once: five waves of queueing — the slowest fan waits 13+ s to be told
  "sold out", and every other sync endpoint (try the calculator mid-sale) is
  stuck in the same queue.
- **Demo mechanics:** **🌊 Open the gates** (`POST /api/flashsale/simulate`)
  spawns 200 threads that hit the real HTTP endpoint via httpx. The UI polls
  `GET /api/flashsale/results` (async, so it stays live while the thread pool
  drowns) and renders per-fan status dots plus wait-time stats.
- **Tests:** `tests/unit/test_flashsale.py` — **all pass.** Buying works,
  selling out works. Nothing asks "for how many people at once?"
- **Fix:** none shipped, by design. The lesson is the practice: a **load test**
  (Locust, k6, JMeter) that finds the cliff *before* launch day.
- **Lesson:** functional tests prove it works; only a load test proves it works
  *at scale*. One user working ≠ 200 users working.
