from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend import booking, calculator, checkout, flashsale, pizzashop, users

app = FastAPI(title="Why We Write Tests")

FRONTEND = Path(__file__).parent.parent / "frontend" / "index.html"

OPS = {
    "add": calculator.add,
    "subtract": calculator.subtract,
    "multiply": calculator.multiply,
    "divide": calculator.divide,
}


class CalcInput(BaseModel):
    a: float
    b: float
    op: str


class BookInput(BaseModel):
    seat: str
    user: str


class UserInput(BaseModel):
    username: str
    password: str


class Cart(BaseModel):
    items: dict[str, int]
    code: str = ""


class PizzaCart(BaseModel):
    items: dict[str, int]


class ShipInput(BaseModel):
    version: int


class BuyInput(BaseModel):
    user: str


@app.get("/")
def home():
    return FileResponse(FRONTEND)


# ---- demo 1: calculator ----
@app.post("/api/calc")
def calc(inp: CalcInput):
    return {"result": OPS[inp.op](inp.a, inp.b)}


# ---- demo 2: movie seats ----
@app.get("/api/seats")
def seats():
    return booking.all_seats()


@app.post("/api/book")
def book(inp: BookInput):
    return booking.book_seat(inp.seat, inp.user)


@app.get("/api/ticket")
def get_ticket(seat: str, user: str):
    return booking.ticket(seat, user)


# ---- demo 3: login ----
@app.post("/api/signup")
def signup(inp: UserInput):
    return users.signup(inp.username, inp.password)


@app.post("/api/login")
def login(inp: UserInput):
    return users.login(inp.username, inp.password)


# ---- demo 4: snack shop ----
@app.get("/api/products")
def products():
    return checkout.PRODUCTS


@app.post("/api/preview")
def preview(cart: Cart):
    total = checkout.cart_total(cart.items)
    return {"total": total, "after_discount": checkout.apply_discount(total, cart.code)}


@app.post("/api/pay")
def pay(cart: Cart):
    return checkout.pay(cart.items, cart.code)


# ---- demo 5: pizza shop v2 ----
@app.get("/api/pizzashop/state")
def pizzashop_state():
    return {
        "products": pizzashop.PRODUCTS,
        "version": pizzashop.version,
        "combo_price": pizzashop.COMBO_PRICE,
    }


@app.post("/api/pizzashop/preview")
def pizzashop_preview(cart: PizzaCart):
    return {"total": pizzashop.cart_total(cart.items), "version": pizzashop.version}


@app.post("/api/pizzashop/pay")
def pizzashop_pay(cart: PizzaCart):
    return pizzashop.pay(cart.items)


@app.post("/api/pizzashop/ship")
def pizzashop_ship(inp: ShipInput):
    return {"version": pizzashop.ship(inp.version)}


@app.get("/api/pizzashop/code")
def pizzashop_code():
    return pizzashop.source_code()


# ---- demo 6: flash sale ----
# /buy is a sync endpoint on purpose: every request occupies a worker thread
# for the whole payment delay. /status and /results are async so the UI can
# keep polling while the thread pool is drowning.
@app.post("/api/flashsale/buy")
def flashsale_buy(inp: BuyInput):
    return flashsale.buy(inp.user)


@app.post("/api/flashsale/simulate")
async def flashsale_simulate(request: Request):
    return flashsale.simulate(str(request.base_url))


@app.get("/api/flashsale/status")
async def flashsale_status():
    return {"total": flashsale.TICKETS, "left": flashsale.tickets_left}


@app.get("/api/flashsale/results")
async def flashsale_results():
    return flashsale.sim


# ---- reset everything, demo again ----
@app.post("/api/reset")
def reset():
    booking.reset_db()
    users.reset_db()
    checkout.reset()
    pizzashop.reset()
    flashsale.reset()
    return {"ok": True}


booking.reset_db()
users.reset_db()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", port=1184, reload=True)
