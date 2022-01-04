from fastapi import FastAPI

from app.core.business_logic.manager_report import IReportCommand, XReportCommand, Reporter
from app.core.business_logic.point_of_sales import PointOfSales
from app.core.persistence.repository import IPOSRepository, SqlLiteRepository, IReportRepository
from app.infra.fastapi.endpoints import cashier_api, customer_api, manager_api


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(cashier_api.cashier_api, prefix="/cashier", tags=["Cashier"])
    app.include_router(customer_api.customer_api, prefix="/customer", tags=["Customer"])
    app.include_router(manager_api.manager_api, prefix="/manager", tags=["Manager"])

    app.state.repository = setup_sql_lite_repository()
    app.state.pos = setup_pos(app.state.repository)
    app.state.reporter = setup_reporter(setup_x_report(app.state.repository))

    return app


# setup service beans
def setup_sql_lite_repository() -> SqlLiteRepository:
    return SqlLiteRepository(r"C:\Users\besik.kapanadze\Desktop\Freeuni-Stuff\Design-Patterns\design-patterns-ass-4"
                             r"\disk.db")


def setup_pos(repository: IPOSRepository) -> PointOfSales:
    return PointOfSales(repository)


def setup_x_report(repository: IReportRepository) -> IReportCommand:
    return XReportCommand(repository)


def setup_reporter(x_report: IReportCommand) -> Reporter:
    return Reporter(x_report=x_report)
