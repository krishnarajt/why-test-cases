# Why We Write Tests

An interactive demo for teaching the value of test cases: six small apps, each
hiding one intentional bug, each showing why a different layer of testing exists.

> **Instructors / AI agents:** every bug is documented in [BUGS.md](BUGS.md).
> Keep it off the projector — the audience should guess.

## Quick start

```bash
cd why_test_cases
uv sync
uv run uvicorn backend.main:app --port 1184 --reload
```

Open **http://localhost:1184** — that's the whole show. Every restart (and every
code reload) starts with a fresh database.

To wipe state mid-demo without restarting, click **Reset demo data** in the UI, or:

```bash
curl -X POST http://localhost:1184/api/reset
```

To stop the server, press **Ctrl+C** in its terminal — or, if it's running in
the background:

```bash
pkill -f "uvicorn backend.main:app"
```

## The six demos

| # | Tab | Bug lives in | Unit tests | Integration tests | Caught by |
|---|-----|-------------|------------|-------------------|-----------|
| 1 | Calculator | backend | none (empty file) | none | any unit test at all |
| 2 | Seat Booking | backend (race) | all pass | commented out — FAIL when enabled | an integration test |
| 3 | Login | backend (DB constraint) | all pass | commented out — FAIL when enabled | an integration test |
| 4 | Checkout | **frontend** | all pass | commented out — PASS when enabled | a manual test run |
| 5 | Pizza Shop v2 | backend (a v2 "refactor") | all pass | — | **a manual regression pass** |
| 6 | Flash Sale | nowhere — that's the point | all pass | — | **a load test** |

Each tab in the UI has a "Demo walkthrough" card with click-by-click steps
(including the 2–4 second race window for the seat booking demo).

Demos 5 and 6 deliberately ship **no fix**: their lesson is a practice, not a
patch. Demo 5's tab has a live **"🚀 Ship v2"** button and a release checklist —
the manual regression pass, made visible. Demo 6's tab unleashes 200 simulated
fans on the real HTTP endpoint and charts the meltdown live (while it runs, try
the Calculator tab — the whole site is stuck in the same queue).

## Test commands

```bash
# 1. Calculator — nothing runs, the file is empty
uv run pytest tests/unit/test_calculator.py

# 2. Seat booking — unit tests all green
uv run pytest tests/unit/test_booking.py
uv run pytest tests/integration/test_booking.py   # uncomment the file to watch it fail

# 3. Login — unit tests all green
uv run pytest tests/unit/test_users.py
uv run pytest tests/integration/test_users.py     # uncomment the file to watch it fail

# 4. Checkout — everything is green, and the app is still broken
uv run pytest tests/unit/test_checkout.py
uv run pytest tests/integration/test_checkout.py  # uncomment the file — it PASSES

# 5. Pizza shop — all green: v1 flows tested on v1, the combo tested on v2.
#    Nobody re-tests the old flows on the new code.
uv run pytest tests/unit/test_pizzashop.py

# 6. Flash sale — all green. None of them asks "for how many people at once?"
uv run pytest tests/unit/test_flashsale.py
```

## Suggested live flow (per demo)

1. Show the app working, then trigger the bug in the UI (steps are in each tab).
2. Let the audience guess what's wrong.
3. Demos 1–3: uncomment the relevant test file, run it, watch it fail.
   Demo 4: watch everything pass while the app stays broken.
   Demo 5: the bug is on screen — the tab shows the shipped function, live from
   the server. Walk the release checklist instead of a test file.
   Demo 6: there is nothing to uncomment — the code is fine; the scale wasn't.
4. Demos 1–4 only: hand it to a coding agent — *"this test fails, fix the code"* —
   re-run the tests, then re-demo the UI working. (5 and 6 have no fix by design:
   the lesson is the regression pass and the load test, not a patch.)

## Static site (no backend)

`demo-site/index.html` is a self-contained, deploy-anywhere version — the same
six exhibits with simulated apps, code panels, and the checks that catch each
bug. Same look as the live demo, one exhibit after another as you scroll.
Deploy the `demo-site/` folder to Vercel as-is, or preview locally:

```bash
python3 -m http.server 1185 --directory demo-site
# → http://localhost:1185
# stop it with Ctrl+C, or:  pkill -f "http.server 1185"
```

## Layout

```
backend/            FastAPI app (main.py) + one small module per demo
frontend/           index.html — the live demo UI (served by the backend)
tests/unit/         fast, isolated tests
tests/integration/  tests that go through the real DB / real API
demo-site/          standalone static site for Vercel
BUGS.md             spoilers: every bug (for the instructor & the agent)
```
