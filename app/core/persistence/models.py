import dataclasses
from abc import ABC, abstractmethod
from typing import List


class Sellable(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_price(self) -> float:
        pass


@dataclasses.dataclass
class SingleItem(Sellable):
    name: str
    price: float

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.price


@dataclasses.dataclass
class Pack(Sellable):
    name: str
    quantity: int
    sellable: Sellable

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.quantity * self.sellable.get_price()


@dataclasses.dataclass
class CountedItem:
    item: Sellable
    count: int

    def get_total_price(self) -> float:
        return self.count * self.item.get_price()


@dataclasses.dataclass
class Receipt:
    id: int
    closed: bool
    open_date: str
    items: List[CountedItem]

    def __iter__(self):
        return iter(self.items)
