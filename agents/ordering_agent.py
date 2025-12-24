import requests, json, re
from agents.a2a_protocol import send_message

from config import settings

MCP_URL = settings.MCP_URL 


# ---------- Fallback parser ----------
def fallback_extract(text: str):
    text = text.lower()

    pizzas = {
        "margherita": "Margherita",
        "farmhouse": "Farmhouse",
        "pepperoni": "Pepperoni",
        "veg supreme": "Veg Supreme"
    }

    pizza = "Margherita"
    for key, value in pizzas.items():
        if key in text:
            pizza = value
            break

    size = "Medium"
    if "large" in text:
        size = "Large"
    elif "small" in text:
        size = "Small"

    return {"pizza": pizza, "size": size}


# ---------- MULTI-ORDER SUPPORT ----------
def ordering_agent(user_text: str):
    """
    Supports multiple pizzas in one checkout.
    Example input:
    'farmhouse medium, pepperoni small, pepperoni small'
    """

    items = [t.strip() for t in user_text.split(",")]

    placed_orders = []

    for item in items:
        order = fallback_extract(item)

        response = requests.post(
            f"{MCP_URL}/mcp/place_order",
            json=order
        ).json()

        if "order_id" not in response:
            raise ValueError(f"Failed to place order for: {item}")

        placed_orders.append(response)

    # Send A2A message with all orders
    send_message(
        "OrderingAgent",
        "SchedulingAgent",
        placed_orders
    )

    return {
        "order_ids": [o["order_id"] for o in placed_orders],
        "eta": placed_orders[0]["eta"],
        "items": len(placed_orders)
    }
