from fastapi import APIRouter

manager_api = APIRouter()


@manager_api.get("/report/{report_type}")
def request_receipt(report_type: str) -> str:
    return f'{report_type} Report'
