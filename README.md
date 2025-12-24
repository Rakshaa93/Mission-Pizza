#  Pizza AI Agent System

**An AI-powered pizza ordering system with multi-agent orchestration using MCP (Model Context Protocol)**

---

## 📋 Table of Contents

- [Overview](#Overview)
- [Architecture](#architecture)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Agent Communication Flow](#agent-communication-flow)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

---

##  Overview

This system demonstrates automated transformation of OpenAPI specifications into MCP servers, enabling AI agents to interact with pizza ordering services. Two cooperating agents handle order placement and delivery scheduling through Agent-to-Agent (A2A) communication.

### Key Components

1. **OpenAPI to MCP Converter** - Automatically generates MCP tools from OpenAPI specs
2. **Ordering Agent** - Handles pizza orders via natural language
3. **Scheduling Agent** - Coordinates delivery timing via external calendar MCP
4. **Web UI** - User-friendly chat interface for placing orders

---

##  Architecture

```
┌─────────────────┐
│   Web UI        │
│  (Frontend)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   UI Server     │
│  (FastAPI)      │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌──────────────┐
│Ordering │ │  Scheduling  │
│ Agent   │─│    Agent     │
└────┬────┘ └──────┬───────┘
     │             │
     │      A2A Protocol
     │             │
     ▼             ▼
┌─────────────┐ ┌──────────────┐
│ MCP Server  │ │Calendar MCP  │
│  (Pizza)    │ │  (External)  │
└─────────────┘ └──────────────┘
```

### Communication Flow

1. User submits order via web chat
2. UI Server routes to Ordering Agent
3. Ordering Agent calls MCP Server to place order
4. Ordering Agent sends A2A message to Scheduling Agent
5. Scheduling Agent calls external Calendar MCP
6. Confirmation returned to user

---

## ✨ Features

- ✅ Automatic OpenAPI → MCP conversion
- ✅ Multi-pizza ordering support
- ✅ Natural language processing
- ✅ Agent-to-Agent communication protocol
- ✅ Real-time order tracking
- ✅ Delivery scheduling integration
- ✅ Beautiful chat UI

---

##  Setup Instructions

### Prerequisites

- Python 3.9+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PIZZA
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

### Running the System

**Option 1: Single Command (Recommended)**
```bash
python start_system.py
```

**Option 2: Manual Start (For Development)**
```bash
# Terminal 1 - MCP Server
uvicorn backend.mcp_server:app --port 8001

# Terminal 2 - Calendar MCP
uvicorn external_mcp.mock_calendar_mcp:app --port 8002

# Terminal 3 - UI Server
uvicorn ui_server:app --port 9000
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:9000
```

---

##  Usage

### Basic Order Flow

1. **Enter your name** when prompted
2. **Provide location** for delivery
3. **View menu** by typing `menu`
4. **Add pizzas** by typing pizza name and size:
   ```
   margherita medium
   pepperoni large
   farmhouse small x2
   ```
5. **Checkout** by typing `checkout` or `place order`

### Example Conversation

```
Bot: Hi! What is your name?
You: Rakshaa

Bot: Nice to meet you, Rakshaa! 📍 Where are you located?
You: Mumbai

Bot: Great! You can now order pizza...
You: menu

Bot: Available Pizzas:
     • Margherita (Small, Medium, Large)
     • Farmhouse (Medium, Large)
     ...

You: farmhouse medium
Bot: Added "farmhouse medium" to your order.

You: pepperoni small x2
Bot: Added "pepperoni small" (2 items) to your order.

You: checkout
Bot: 🍕 Hi Rakshaa! Your order is confirmed...
```

---

##  API Documentation

### MCP Server Endpoints

#### `GET /mcp/menu`
Returns available pizzas and sizes.

**Response:**
```json
{
  "Margherita": ["Small", "Medium", "Large"],
  "Farmhouse": ["Medium", "Large"],
  "Pepperoni": ["Medium", "Large"],
  "Veg Supreme": ["Small", "Medium", "Large"]
}
```

#### `POST /mcp/place_order`
Places a pizza order.

**Request:**
```json
{
  "pizza": "Margherita",
  "size": "Medium"
}
```

**Response:**
```json
{
  "order_id": "uuid-string",
  "eta": "30 minutes"
}
```

#### `GET /mcp/track_order/{order_id}`
Tracks order status.

**Response:**
```json
{
  "pizza": "Margherita",
  "size": "Medium",
  "status": "Preparing",
  "eta": "30 minutes"
}
```

### UI Server Endpoints

#### `GET /menu`
Fetches menu from MCP server.

#### `POST /order`
Places order through agent system.

**Request:**
```json
{
  "text": "margherita medium, pepperoni small",
  "name": "John",
  "location": "Mumbai"
}
```

---

##  Agent Communication Flow

### A2A Protocol Message Structure

```python
{
  "from": "OrderingAgent",
  "to": "SchedulingAgent",
  "payload": {
    "order_ids": ["uuid1", "uuid2"],
    "eta": "30 minutes",
    "items": 2
  }
}
```

### Agent Responsibilities

| Agent | Responsibilities |
|-------|------------------|
| **Ordering Agent** | • Parse user input<br>• Validate orders<br>• Call MCP server<br>• Send A2A messages |
| **Scheduling Agent** | • Receive order info<br>• Call calendar MCP<br>• Schedule delivery<br>• Return confirmation |

---

##  Project Structure

```
PIZZA/
├── agents/                    # AI Agent implementations
│   ├── a2a_protocol.py       # Agent-to-Agent messaging
│   ├── ordering_agent.py     # Pizza ordering logic
│   └── scheduling_agent.py   # Delivery scheduling
│
├── backend/                   # MCP Server & API
│   ├── mcp_server.py         # Generated MCP server
│   ├── openapi_to_mcp.py     # OpenAPI → MCP converter
│   └── openapi.yaml          # Pizza API specification
│
├── external_mcp/              # External MCP services
│   └── mock_calendar_mcp.py  # Calendar scheduling mock
│
├── frontend/                  # Web UI
│   ├── chat.css              # Styling
│   ├── chat.js               # Client-side logic
│   └── index.html            # Chat interface
│
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── start_system.py           # System launcher
└── ui_server.py              # Main API gateway
```

---

##  Technologies Used

- **FastAPI** - High-performance web framework
- **Uvicorn** - ASGI server
- **Requests** - HTTP client library
- **PyYAML** - YAML parsing for OpenAPI specs
- **Pydantic** - Data validation
- **JavaScript** - Frontend interactivity
- **CSS3** - Modern styling

---

##  Future Enhancements

- [ ] Add authentication & authorization
- [ ] Implement persistent database (PostgreSQL/MongoDB)
- [ ] Add real-time order tracking via WebSockets
- [ ] Integrate payment processing
- [ ] Add more external MCP servers (SMS, Email)
- [ ] Implement comprehensive error handling
- [ ] Add unit and integration tests
- [ ] Deploy to cloud (AWS/GCP/Azure)

---

##  Troubleshooting

### Issue: Ports already in use
```bash
# Kill processes on specific ports
lsof -ti:8001 | xargs kill -9
lsof -ti:8002 | xargs kill -9
lsof -ti:9000 | xargs kill -9
```

### Issue: Module not found errors
```bash
# Ensure you're in virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Cannot connect to MCP servers
- Verify all three servers are running
- Check console for error messages
- Ensure no firewall blocking localhost connections

---

##  License

This project is licensed under the MIT License.

---


##  Contact

For questions or issues, please contact [rakshaa9302@gmail.com].

---
