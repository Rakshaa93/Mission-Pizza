from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from config import settings
from agents.ordering_agent import ordering_agent
from agents.scheduling_agent import scheduling_agent
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def home():
    return FileResponse("frontend/index.html")

class Order(BaseModel):
    text: str
    name: str 
    location: str 

@app.get("/menu")
def fetch_menu():
    response = requests.get(f"{settings.MCP_URL}/mcp/menu")
    return response.json()

@app.post("/order")
def order_pizza(req: Order):
    order_info = ordering_agent(req.text)
    schedule = scheduling_agent(order_info)

    user_name = req.name or "Customer"
    user_location = req.location or "your location"

    # Handle multiple orders
    order_ids = ", ".join(order_info["order_ids"])
    total_items = order_info["items"]

    message = (
        f"🍕 Hi {user_name}! Your order is confirmed.\n\n"
        f"📍 Delivery Location: {user_location}\n\n"
        f"• Order IDs: {order_ids}\n"
        f"• Total items: {total_items}\n"
        f"• Estimated time: {order_info['eta']}\n\n"
        f"🚚 Delivery Details:\n"
        f"• Delivery time: {schedule['delivery_time']}\n"
        f"• Event: {schedule['calendar_event']['event']}\n\n"
        f"👨‍🍳 Note from Chef:\n"
        f"{schedule['note']}\n\n"
        f"✅ Status Updates:\n"
        f"- All items confirmed\n"
        f"- Delivery scheduled\n"
        f"- You will be notified when it’s out for delivery"
    )

    return {"message": message}
