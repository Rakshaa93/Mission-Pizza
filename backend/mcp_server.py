from fastapi import FastAPI
from backend.openapi_to_mcp import generate_mcp_tools
import uuid

app = FastAPI()
TOOLS = generate_mcp_tools("backend/openapi.yaml")

ORDERS = {}
MENU = {
    "Margherita": ["Small", "Medium", "Large"],
    "Farmhouse": ["Medium", "Large"],
    "Pepperoni": ["Medium", "Large"],
    "Veg Supreme": ["Small", "Medium", "Large"]
}

@app.get("/mcp/menu")
def get_menu():
    return MENU

@app.get("/mcp/tools")
def list_tools():
    return TOOLS

@app.post("/mcp/place_order")
def place_order(data: dict):
    pizza = data["pizza"]
    size = data["size"]

    if pizza not in MENU:
        return {"error": "Pizza not available"}

    if size not in MENU[pizza]:
        return {"error": f"{size} size not available for {pizza}"}

    order_id = str(uuid.uuid4())
    ORDERS[order_id] = {
        "pizza": pizza,
        "size": size,
        "status": "Preparing",
        "eta": "30 minutes"
    }

    return {"order_id": order_id, "eta": "30 minutes"}

@app.get("/mcp/track_order/{order_id}")
def track_order(order_id: str):
    return ORDERS.get(order_id, {"error": "Order not found"})

@app.post("/mcp/update_status/{order_id}")
def update_status(order_id: str, status: str):
    if order_id in ORDERS:
        ORDERS[order_id]["status"] = status
        return {"status": status}
    return {"error": "Order not found"}
