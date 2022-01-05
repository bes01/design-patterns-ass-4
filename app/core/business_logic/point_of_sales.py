from typing import Protocol, Tuple

from fastapi import HTTPException

from app.core.persistence.models import Receipt
from app.core.persistence.repository import IPOSRepository


class ICustomerPointOfSales(Protocol):
    def get_receipt(self, receipt_id: int) -> Tuple[Receipt, int]:
        pass


class ICashierPointOfSales(Protocol):
    def open_receipt(self) -> int:
        pass

    def add_item_to_receipt(self, receipt_id: int, item_id: int, quantity: int) -> None:
        pass

    def close_receipt(self, receipt_id: int) -> None:
        pass


class PointOfSales:
    def __init__(self, repository: IPOSRepository) -> None:
        self._repository = repository

    def open_receipt(self) -> int:
        if self._repository.open_receipt_exists():
            raise HTTPException(status_code=409, detail="Cannot open second receipt!")
        return self._repository.create_receipt()

    def add_item_to_receipt(self, receipt_id: int, item_id: int, quantity: int) -> None:
        if quantity <= 0:
            raise HTTPException(status_code=409, detail="Illegal quantity parameter!")
        if not self._repository.receipt_exists(receipt_id, False):
            raise HTTPException(
                status_code=409, detail="Can't find open receipt with passed id!"
            )
        self._repository.add_item(receipt_id, item_id, quantity)

    def close_receipt(self, receipt_id: int) -> None:
        self._repository.close_receipt(receipt_id)

    def get_receipt(self, receipt_id: int) -> Tuple[Receipt, float]:
        receipt = self._repository.get_receipt(receipt_id)
        total = sum([item.sum_price for item in receipt])
        return receipt, total
