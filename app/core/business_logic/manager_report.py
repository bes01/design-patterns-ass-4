from typing import Protocol

from app.core.business_logic.report_type import ReportType
from app.core.persistence.repository import IReportRepository


class IReportCommand(Protocol):

    def report(self) -> str:
        pass


class XReportCommand:

    def __init__(self, repository: IReportRepository) -> None:
        self._repository = repository

    def report(self) -> str:
        receipts = self._repository.get_current_day_receipts()
        items = []
        for receipt in receipts:
            items += receipt.items
        items.sort(key=lambda x: x.id)

        result = "Items Sold: "

        total_cost = 0
        for i in range(len(items)):
            total_cost += items[i].price * items[i].quantity
            result += f"{items[i].name} {items[i].quantity}x {items[i].price * items[i].quantity}$ | "

        result += f"Total receipts: {len(receipts)} | " \
                  f"Total cost: {total_cost} |"

        return result


class Reporter:

    def __init__(self, *, x_report: IReportCommand):
        self._report_services = {ReportType.X_REPORT: x_report}

    def make_report(self, report_type: ReportType) -> str:
        return self._report_services[report_type].report()
