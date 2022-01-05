from fastapi import APIRouter, Depends

from app.core.facade import ICustomerPointOfSales
from app.infra.fastapi.dependables import get_pos
from app.infra.fastapi.dto.receipt_response import ReceiptResponse

customer_api = APIRouter()


@customer_api.get("/receipt/{receipt_id}")
def request_receipt(
    receipt_id: int, pos: ICustomerPointOfSales = Depends(get_pos)
) -> ReceiptResponse:
    return ReceiptResponse(*pos.get_receipt(receipt_id))
