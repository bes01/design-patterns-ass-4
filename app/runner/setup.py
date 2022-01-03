from fastapi import FastAPI

from app.api import cashier, customer, manager


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(cashier.cashier_api, prefix="/cashier", tags=["Cashier"])
    app.include_router(customer.customer_api, prefix="/customer", tags=["Customer"])
    app.include_router(manager.manager_api, prefix="/manager", tags=["Manager"])
    return app
