from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from routes import menu

app = FastAPI()

# ✅ Enable CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Store connected kitchen clients
clients = []

# 🔌 WebSocket endpoint (for kitchen screen)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep connection alive
    except:
        clients.remove(websocket)

# 🍔 Order API (frontend sends order here)
@app.post("/order")
async def create_order(order: dict):
    # 🔥 Send order to all kitchen screens
    for client in clients:
        await client.send_json(order)   # ✅ proper JSON (no hack needed)
    return {"message": "Order sent to kitchen"}

# 📋 Menu API (optional)
app.include_router(menu.router)

# 🏠 Home route
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}
