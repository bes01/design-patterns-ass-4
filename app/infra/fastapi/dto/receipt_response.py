from dataclasses import dataclass

from app.core.persistence.models import Receipt


@dataclass
class ReceiptResponse:
    receipt: Receipt
    total: float
