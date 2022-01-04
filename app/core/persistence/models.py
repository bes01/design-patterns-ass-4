import dataclasses
from typing import List


@dataclasses.dataclass
class Item:
    id: int
    name: str
    price: float
    parent_item_id: int
    quantity: int


@dataclasses.dataclass
class Receipt:
    id: int
    closed: bool
    open_date: str
    items: List[Item]
