import requests
from agents.a2a_protocol import send_message
from config import settings

CALENDAR_MCP = settings.CALENDAR_MCP_URL

def scheduling_agent(order_info):
    send_message("OrderingAgent", "SchedulingAgent", order_info)

    delivery_time = "Today + 30 minutes"

    calendar_event = requests.post(
        f"{CALENDAR_MCP}/mcp/schedule",
        json={"time": delivery_time}
    ).json()

    return {
        "delivery_time": delivery_time,
        "calendar_event": calendar_event,
        "note": "Chef recommends today’s special topping ✨"
    }
