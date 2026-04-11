from fastapi import APIRouter

router = APIRouter()

orders = []   # temporary storage

@router.post("/order")
def create_order(order: dict):
    orders.append(order)
    return {"message": "Order placed successfully"}

@router.get("/orders")
def get_orders():
    return orders