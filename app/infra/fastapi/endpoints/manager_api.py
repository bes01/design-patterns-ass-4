from fastapi import APIRouter, Depends

from app.core.business_logic.manager_report import Reporter
from app.core.business_logic.report_type import ReportType
from app.infra.fastapi.dependables import get_reporter

manager_api = APIRouter()


@manager_api.get("/report/{report_type}")
def request_receipt_report(
    report_type: ReportType, reporter: Reporter = Depends(get_reporter)
) -> str:
    return reporter.make_report(report_type)
