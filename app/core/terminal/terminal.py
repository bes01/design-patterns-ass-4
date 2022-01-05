from typing import Protocol, Tuple

from fastapi import HTTPException

from app.core.models import Receipt
from app.infra.persistence.persistence_exception import RecordNotFoundException


class ITerminalRepository(Protocol):
    def create_receipt(self) -> int:
        pass

    def open_receipt_exists(self) -> bool:
        pass

    def add_item(self, receipt_id: int, item_id: int, quantity: int) -> None:
        pass

    def close_receipt(self, receipt_id: int) -> None:
        pass

    def get_receipt(self, receipt_id: int) -> Receipt:
        pass

    def receipt_exists(self, receipt_id: int, closed: bool) -> bool:
        pass

    def item_exists(self, item_id: int) -> bool:
        pass


class TerminalInteractor:
    def __init__(self, repository: ITerminalRepository) -> None:
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
                status_code=404, detail="Can't find open receipt with passed id!"
            )
        if not self._repository.item_exists(item_id):
            raise HTTPException(
                status_code=404, detail="Can't find item with passed id!"
            )
        self._repository.add_item(receipt_id, item_id, quantity)

    def close_receipt(self, receipt_id: int) -> None:
        try:
            self._repository.close_receipt(receipt_id)
        except RecordNotFoundException as ex:
            raise HTTPException(status_code=404, detail=ex.message)

    def get_receipt(self, receipt_id: int) -> Tuple[Receipt, float]:
        try:
            receipt = self._repository.get_receipt(receipt_id)
            total = sum([item.sum_price for item in receipt])
            return receipt, total
        except RecordNotFoundException as ex:
            raise HTTPException(status_code=404, detail=ex.message)
