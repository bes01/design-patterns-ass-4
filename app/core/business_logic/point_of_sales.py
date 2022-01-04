from typing import Protocol, Tuple

from app.core.persistence.models import Receipt
from app.core.persistence.repository import IPOSRepository


class ICustomerPointOfSales(Protocol):
    def get_receipt(self, receipt_id: int) -> Tuple[Receipt, int]:
        pass


class ICashierPointOfSales(Protocol):
    def open_receipt(self) -> int:
        pass

    def add_item_to_receipt(self, receipt_id, item_id, quantity) -> None:
        pass

    def close_receipt(self, receipt_id) -> None:
        pass


class PointOfSales:

    def __init__(self, repository: IPOSRepository) -> None:
        self._repository = repository

    def open_receipt(self) -> int:
        if self._repository.open_receipt_exists():
            raise Exception("Cannot open second receipt!")
        return self._repository.create_receipt()

    def add_item_to_receipt(self, receipt_id, item_id, quantity) -> None:
        if quantity <= 0:
            raise Exception("Illegal parameter")
        self._repository.add_item(receipt_id, item_id, quantity)

    def close_receipt(self, receipt_id) -> None:
        self._repository.close_receipt(receipt_id)

    def get_receipt(self, receipt_id: int) -> Tuple[Receipt, int]:
        receipt = self._repository.get_receipt(receipt_id)
        total = sum([item.price * item.quantity for item in receipt.items])
        return receipt, total
