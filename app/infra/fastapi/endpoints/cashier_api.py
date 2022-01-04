from fastapi import APIRouter, Depends

from app.core.business_logic.point_of_sales import ICashierPointOfSales
from app.infra.fastapi.dependables import get_pos

cashier_api = APIRouter()


@cashier_api.post("/receipt/open")
def open_receipt(pos: ICashierPointOfSales = Depends(get_pos)) -> int:
    return pos.open_receipt()


@cashier_api.post("/receipt/{receipt_id}/add/item/{item_id}")
def add_item(receipt_id: int, item_id: int, quantity: int = 1,
             pos: ICashierPointOfSales = Depends(get_pos)) -> None:
    pos.add_item_to_receipt(receipt_id, item_id, quantity)


@cashier_api.post("/receipt/{receipt_id}/close")
def close_receipt(receipt_id: int, pos: ICashierPointOfSales = Depends(get_pos)) -> None:
    pos.close_receipt(receipt_id)
