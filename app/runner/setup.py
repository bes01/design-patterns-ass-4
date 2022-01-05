from fastapi import FastAPI

from app.core.facade import PointOfSales
from app.core.manager.manager_report import (
    IReportCommand,
    ReporterInteractor,
    XReportCommand,
)
from app.core.terminal.terminal import TerminalInteractor
from app.infra.fastapi.endpoints import cashier_api, customer_api, manager_api
from app.infra.persistence.repository import (
    IReporterRepository,
    ITerminalRepository,
    SqlLiteRepository,
)
from app.runner.settings import DB_LOCATION


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(cashier_api.cashier_api, prefix="/cashier", tags=["Cashier"])
    app.include_router(customer_api.customer_api, prefix="/customer", tags=["Customer"])
    app.include_router(manager_api.manager_api, prefix="/manager", tags=["Manager"])

    app.state.repository = setup_sql_lite_repository()
    app.state.terminal = setup_terminal(app.state.repository)
    app.state.manager_reporter = setup_reporter(setup_x_report(app.state.repository))
    app.state.point_of_sales = setup_pos(app.state.terminal, app.state.manager_reporter)

    return app


# Setup Service Beans
def setup_pos(
    terminal: TerminalInteractor, reporter: ReporterInteractor
) -> PointOfSales:
    return PointOfSales(terminal, reporter)


def setup_sql_lite_repository() -> SqlLiteRepository:
    return SqlLiteRepository(DB_LOCATION)


def setup_terminal(repository: ITerminalRepository) -> TerminalInteractor:
    return TerminalInteractor(repository)


def setup_x_report(repository: IReporterRepository) -> IReportCommand:
    return XReportCommand(repository)


def setup_reporter(x_report: IReportCommand) -> ReporterInteractor:
    return ReporterInteractor(x_report=x_report)
