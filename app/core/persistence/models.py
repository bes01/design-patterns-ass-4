import dataclasses
from abc import ABC, abstractmethod
from typing import Iterator, List


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
class ItemGroup(Sellable):
    name: str
    items: List[Sellable]

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return sum([item.get_price() for item in self.items])


@dataclasses.dataclass
class CountedItem:
    item: Sellable
    count: int
    sum_price: int


@dataclasses.dataclass
class Receipt:
    id: int
    closed: bool
    open_date: str
    items: List[CountedItem]

    def __iter__(self) -> Iterator[CountedItem]:
        return iter(self.items)
