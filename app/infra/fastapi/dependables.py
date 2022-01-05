from starlette.requests import Request

from app.core.business_logic.manager_report import Reporter
from app.core.business_logic.point_of_sales import PointOfSales


def get_pos(request: Request) -> PointOfSales:
    return request.app.state.point_of_sales


def get_reporter(request: Request) -> Reporter:
    return request.app.state.manager_reporter
