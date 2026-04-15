from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from routes import menu
from datetime import datetime
from routes.orders import router as orders_router
import uuid

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Store connected kitchen clients
clients = []

# 🔥 STORE ORDERS (THIS WAS MISSING)
orders = []

# 🔌 WebSocket endpoint (for kitchen screen)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        clients.remove(websocket)

# 🍔 Order API (frontend sends order here)
@app.post("/order")
async def create_order(order: dict):

    # ✅ CREATE STRUCTURED ORDER
    new_order = {
        "id": str(uuid.uuid4()),
        "customer": order.get("customer", "Unknown"),
        "phone": order.get("phone", "N/A"),
        "table": order.get("table", "N/A"),
        "items": order.get("items", []),
        "status": "Preparing",
        "timestamp": datetime.now().isoformat()
    }

    # ✅ STORE ORDER
    orders.append(new_order)

    # ✅ SEND TO WEBSOCKET CLIENTS
    for client in clients:
        await client.send_json(new_order)

    return {
        "message": "Order placed successfully",
        "order_id": new_order["id"]
    }

# 📋 GET ALL ORDERS (FOR ADMIN PANEL)
@app.get("/orders")
def get_orders():
    return orders

# ✅ UPDATE ORDER STATUS
@app.put("/order/{order_id}")
def update_order(order_id: str):
    for order in orders:
        if order["id"] == order_id:
            order["status"] = "Ready"
            return {"message": "Order updated"}
    return {"error": "Order not found"}

# 📋 Menu API
app.include_router(orders_router)

# 🏠 Home route
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

# 🔧 Run
import os
port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)