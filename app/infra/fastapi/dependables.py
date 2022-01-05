from typing import Any

from starlette.requests import Request


def get_pos(request: Request) -> Any:
    return request.app.state.point_of_sales


def get_reporter(request: Request) -> Any:
    return request.app.state.manager_reporter
