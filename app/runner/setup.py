import os

from fastapi import FastAPI

from app.core.persistence.repository import IPOSRepository, POSRepository
from app.infra.fastapi.endpoints import cashier, manager, customer


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(cashier.cashier_api, prefix="/cashier", tags=["Cashier"])
    app.include_router(customer.customer_api, prefix="/customer", tags=["Customer"])
    app.include_router(manager.manager_api, prefix="/manager", tags=["Manager"])

    app.state.repository = setup_pos_repository()

    return app


# setup service beans
def setup_pos_repository() -> IPOSRepository:
    return POSRepository(r"C:\Users\besik.kapanadze\Desktop\Freeuni-Stuff\Design-Patterns\design-patterns-ass-4\disk.db")
