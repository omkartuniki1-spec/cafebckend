from fastapi import APIRouter
from datetime import datetime
import uuid

router = APIRouter()

orders = []   # temporary storage


# ✅ CREATE ORDER
@router.post("/order")
def create_order(order: dict):
    new_order = {
        "id": str(uuid.uuid4()),   # unique order ID
        "customer": order.get("customer", "Unknown"),
        "phone": order.get("phone", "N/A"),
        "table": order.get("table", "N/A"),
        "items": order.get("items", []),
        "status": "Preparing",
        "timestamp": datetime.now().isoformat()
    }

    orders.append(new_order)

    return {
        "message": "Order placed successfully",
        "order_id": new_order["id"]
    }


# ✅ GET ALL ORDERS
@router.get("/orders")
def get_orders():
    return orders


# ✅ UPDATE ORDER STATUS (VERY IMPORTANT FOR ADMIN PANEL)
@router.put("/order/{order_id}")
def update_order_status(order_id: str):
    for order in orders:
        if order["id"] == order_id:
            order["status"] = "Ready"
            return {"message": "Order updated"}

    return {"error": "Order not found"}