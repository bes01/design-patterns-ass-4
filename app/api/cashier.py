import random

from fastapi import APIRouter

cashier_api = APIRouter()


@cashier_api.post("/receipt/open")
def open_receipt() -> str:
    return f"opened receipt with uid {random.randint(0, 1000000)}"


@cashier_api.post("/receipt/add/item/{item_name}")
def open_receipt(item_name: str, quantity: int = 1) -> str:
    return f'{item_name} added {quantity} times'


@cashier_api.post("/receipt/close")
def open_receipt() -> str:
    return "close receipt"
