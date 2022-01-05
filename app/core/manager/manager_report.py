import itertools
from typing import Any, Protocol

from app.core.manager.report_type import ReportType
from app.infra.persistence.models import Sellable
from app.infra.persistence.repository import IReporterRepository


class IReportCommand(Protocol):
    def report(self) -> dict[str, Any]:
        pass


class XReportCommand:
    def __init__(self, repository: IReporterRepository) -> None:
        self._repository = repository

    def report(self) -> dict[str, Any]:
        receipts = self._repository.get_current_day_receipts()

        items_sold: dict[int, Any] = {}
        total_receipts = len(receipts)
        total_cost = 0.0

        for counted_item in itertools.chain(*receipts):
            item: Sellable = counted_item.item
            if item.get_unique_identifier() in items_sold:
                items_sold[item.get_unique_identifier()]["units"] += counted_item.count
            else:
                items_sold[item.get_unique_identifier()] = {
                    "name": item.get_name(),
                    "units": counted_item.count,
                }
            total_cost += counted_item.sum_price

        return {
            "items_sold": items_sold,
            "total_receipts": total_receipts,
            "total_cost": total_cost,
        }


class ReporterInteractor:
    def __init__(self, *, x_report: IReportCommand) -> None:
        self._report_services = {ReportType.X_REPORT: x_report}

    def make_report(self, report_type: ReportType) -> dict[str, Any]:
        return self._report_services[report_type].report()
