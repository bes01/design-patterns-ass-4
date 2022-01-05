from dataclasses import dataclass

from app.core.models import Receipt


@dataclass
class ReceiptResponse:
    receipt: Receipt
    total: float
