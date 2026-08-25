import random
import threading
import time

import httpx

TICKETS = 120
FANS = 200
PAYMENT_DELAY = (1.5, 3)  # each purchase spends this long "processing payment"
FAN_PATIENCE = 10  # seconds a simulated fan waits before giving up

_stock_lock = threading.Lock()
tickets_left = TICKETS

# live state of the current simulation, polled by the UI
sim = {"running": False, "fans": []}


def buy(user):
    global tickets_left
    time.sleep(random.uniform(*PAYMENT_DELAY))  # processing payment...
    with _stock_lock:
        if tickets_left > 0:
            tickets_left -= 1
            return {"ok": True, "user": user, "left": tickets_left}
    return {"ok": False, "error": "Sold out", "left": 0}


def simulate(base_url, fans=FANS):
    """Unleash `fans` concurrent buyers on the real HTTP endpoint."""
    if sim["running"]:
        return {"ok": False, "error": "A simulation is already running"}
    sim["running"] = True
    sim["fans"] = [{"id": i, "status": "queued", "ms": None} for i in range(fans)]
    threading.Thread(target=_run_sim, args=(base_url, fans), daemon=True).start()
    return {"ok": True, "fans": fans}


def _run_sim(base_url, fans):
    threads = [
        threading.Thread(target=_one_fan, args=(base_url, i), daemon=True)
        for i in range(fans)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    sim["running"] = False


def _one_fan(base_url, i):
    fan = sim["fans"][i]
    time.sleep(random.uniform(0, 2))  # fans pile in over the first ~2 seconds
    fan["status"] = "buying"
    start = time.monotonic()
    try:
        response = httpx.post(
            f"{base_url}api/flashsale/buy",
            json={"user": f"fan-{i}"},
            timeout=FAN_PATIENCE,
        )
        fan["ms"] = int((time.monotonic() - start) * 1000)
        fan["status"] = "ticket" if response.json().get("ok") else "soldout"
    except Exception:
        fan["ms"] = int((time.monotonic() - start) * 1000)
        fan["status"] = "gaveup"


def reset():
    global tickets_left
    tickets_left = TICKETS
    if not sim["running"]:
        sim["fans"] = []
