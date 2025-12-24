from fastapi import FastAPI

app = FastAPI()

@app.post("/mcp/schedule")
def schedule(data: dict):
    return {
        "event": "Pizza Delivery",
        "scheduled_time": data["time"]
    }
