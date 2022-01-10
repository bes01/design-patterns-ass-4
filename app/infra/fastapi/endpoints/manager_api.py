import datetime
from typing import Any

from fastapi import APIRouter, Depends

from app.core.facade import IManagerPointOfSales
from app.core.manager.report_type import ReportType
from app.infra.fastapi.dependables import get_pos

manager_api = APIRouter()


@manager_api.get("/report/{report_type}")
def request_receipt_report(
    report_day: datetime.date,
    report_type: ReportType,
    pos: IManagerPointOfSales = Depends(get_pos),
) -> dict[str, Any]:
    return pos.get_manager_report(report_day, report_type)
