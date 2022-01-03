from fastapi import APIRouter

customer_api = APIRouter()


@customer_api.get("/receipt")
def request_receipt() -> str:
    return "requested receipt"
