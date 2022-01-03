from starlette.requests import Request

from app.core.persistence.repository import IPOSRepository


def get_pos_repository(request: Request) -> IPOSRepository:
    return request.app.state.repository
