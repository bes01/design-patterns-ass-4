import datetime
from dataclasses import dataclass
from typing import Any, Protocol, Tuple

from app.core.manager.manager_report import ReporterInteractor
from app.core.manager.report_type import ReportType
from app.core.models import Receipt
from app.core.terminal.terminal import TerminalInteractor


class ICustomerPointOfSales(Protocol):
    def get_receipt(self, receipt_id: int) -> Tuple[Receipt, float]:
        pass


class ICashierPointOfSales(Protocol):
    def open_receipt(self) -> int:
        pass

    def add_item_to_receipt(self, receipt_id: int, item_id: int, quantity: int) -> None:
        pass

    def close_receipt(self, receipt_id: int) -> None:
        pass


class IManagerPointOfSales(Protocol):
    def get_manager_report(
        self, report_date: datetime.date, report_type: ReportType
    ) -> dict[str, Any]:
        pass


@dataclass
class PointOfSales:
    _terminal: TerminalInteractor
    _reporter: ReporterInteractor

    def get_receipt(self, receipt_id: int) -> Tuple[Receipt, float]:
        return self._terminal.get_receipt(receipt_id)

    def open_receipt(self) -> int:
        return self._terminal.open_receipt()

    def add_item_to_receipt(self, receipt_id: int, item_id: int, quantity: int) -> None:
        self._terminal.add_item_to_receipt(receipt_id, item_id, quantity)

    def close_receipt(self, receipt_id: int) -> None:
        self._terminal.close_receipt(receipt_id)

    def get_manager_report(
        self, report_date: datetime.date, report_type: ReportType
    ) -> dict[str, Any]:
        return self._reporter.make_report(report_date, report_type)
