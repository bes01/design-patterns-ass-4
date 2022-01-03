import random

from fastapi import APIRouter, Depends

from app.core.persistence.models import Receipt
from app.core.persistence.repository import IPOSRepository
from app.infra.fastapi.dependables import get_pos_repository

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


# TODO: Remove
@cashier_api.get("/test")
def test(repository: IPOSRepository = Depends(get_pos_repository)) -> Receipt:
    return repository.get_receipt(1)
