# Technical Documentation  
## Pizza AI Agent System

### 1.Problem Understanding
The core problem is not pizza ordering, but making traditional APIs usable by AI agents.

Key Challenges Identified:
- REST APIs are not agent-friendly
- Manual MCP creation does not scale
- AI agents require:
  - Structured tools
  - Clear schemas
  - Predictable behavior
- Real-world workflows require multi-agent coordination

Hence, the solution focuses on:

- Automated OpenAPI → MCP translation
- Agent-to-Agent (A2A) workflows
- Graceful handling of ambiguity and partial failures

---
### 2.System Architecture Overview
The system is composed of four logical layers:

#### 2.1 Specification Layer
Input: OpenAPI YAML/JSON
Responsibility:
- Parse endpoints
- Extract request/response schemas
- Generate MCP tool definitions

#### 2.2 MCP Server Layer
Auto-generated MCP server exposes:
- get_menu
- place_order
- track_order

Acts as the single source of truth for pizza operations
Mocked backend data is used intentionally, as allowed by the problem statement 

#### 2.3 Agent Layer
- Ordering Agent
  - Handles natural language input
  - Calls MCP tools
  - Maintains order state
  
-Scheduling Agent
  -Receives order details via A2A
  -Uses an external MCP (calendar mock)
  -Performs delivery coordination

#### 2.4 Interface Layer
- Lightweight web chat UI
- Used only for demonstration
- Not a core evaluation component

---

### 3.OpenAPI → MCP Transformation Logic

#### 3.1 Why Automation Was Necessary
Manual MCP tool creation:
- Is error-prone
- Breaks when APIs change
- Does not scale for large systems

#### 3.2 Transformation Strategy
For each OpenAPI endpoint:
- Endpoint → MCP Tool
- HTTP method → Tool action
- Request schema → MCP input schema
- Response schema → MCP output schema
- Description → Tool metadata

This ensures:
- Full protocol fidelity
- Agent discoverability
- Zero manual MCP coding

#### 3.3 Design Decision
FastAPI was chosen because:
- It natively supports OpenAPI
- Async by default
- Simple introspection for automation

---

### 4. Agent Design Rationale

#### 4.1 Why Multiple Agents?
A multi-agent design was chosen to:
- Enforce separation of concerns
- Enable independent scaling
- Allow future agents (payment, notification)

#### 4.2 Ordering Agent Responsibilities
- Natural language parsing
- Order normalization
- MCP interaction
- Error handling
- A2A message dispatch

#### 4.3 Scheduling Agent Responsibilities
- External MCP interaction
- Delivery time coordination
- Fallback logic when scheduling fails

### 5. Agent-to-Agent (A2A) Communication

#### 5.1 Why A2A?
Direct coupling between agents:
- Reduces flexibility
- Increases failure impact

A2A enables:
- Loose coupling
- Message-based coordination
- Easier extension

#### 5.2 Message Structure
A structured payload is used to ensure:
- Predictable parsing
- Minimal shared state
- Clear responsibility boundaries

---

### 6. Handling Ambiguities (Key Evaluation Area)
The assignment intentionally leaves details vague. The following strategies were implemented:

#### 6.1 Ambiguous User Input
- Incremental clarification
- No irreversible action without confirmation

**Example**:

User: “add one more”
System asks: “Which pizza would you like to add?”

#### 7.2 Quantity Normalization
Supported formats:
- x2
- *2
- 2 margherita
- margherita x 2

All normalized internally into:

{
  "pizza": "Margherita",
  "size": "Medium",
  "quantity": 2
}
