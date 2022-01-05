from dataclasses import dataclass

from app.infra.persistence.models import Receipt


@dataclass
class ReceiptResponse:
    receipt: Receipt
    total: float
