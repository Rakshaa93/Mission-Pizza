# Technical Documentation  
## Pizza AI Agent System

---

## 1. Architectural Choices

### 1.1 Use of MCP (Model Context Protocol)

The system uses **MCP instead of direct REST API calls** to enable AI agents to interact with backend services through structured tools.  
This approach provides:

- A standardized interface for agent-tool interaction  
- Clear input/output schemas for each capability  
- Decoupling between agents and service implementations  
- Easy extensibility for future tools and agents  

Each OpenAPI endpoint is automatically converted into an MCP tool, allowing agents to invoke capabilities without knowing REST details.

---

### 1.2 Multi-Agent Architecture

The system is designed using **multiple specialized agents** rather than a single monolithic agent.

- **Ordering Agent**
  - Parses natural language input
  - Validates pizza name, size, and quantity
  - Communicates with the Pizza MCP server
- **Scheduling Agent**
  - Handles delivery scheduling
  - Communicates with an external Calendar MCP
  - Returns delivery confirmation

This separation ensures:
- Clear responsibility boundaries  
- Easier debugging and testing  
- Simple addition of new agents (payment, notification, analytics)

---

### 1.3 Agent-to-Agent (A2A) Communication

Agents communicate using a lightweight **A2A protocol** instead of shared state.

- Messages contain sender, receiver, and payload
- No direct function calls between agents
- Enables loose coupling and asynchronous workflows

This design mirrors real-world distributed agent systems and avoids tight dependencies.

---

### 1.4 FastAPI as the Core Framework

FastAPI was selected because it:
- Automatically generates OpenAPI specifications
- Supports async operations efficiently
- Integrates well with Pydantic for validation
- Simplifies MCP server generation

This allows seamless OpenAPI → MCP conversion with minimal boilerplate.

---

### 1.5 Mock External MCP Services

External dependencies (like delivery scheduling) are implemented as **mock MCP servers** instead of real third-party APIs.

Benefits:
- No external service dependency
- Fully reproducible local setup
- Focus remains on agent orchestration rather than integrations

---

## 2. Design Assumptions

The system is built with the following assumptions to keep the scope focused:

1. **Single-user interaction**
   - No authentication, sessions, or multi-user concurrency
2. **Static pizza menu**
   - Menu is predefined and served by the MCP server
3. **Limited domain language**
   - User input is constrained to pizza-ordering context
4. **Trusted MCP services**
   - External MCP servers are assumed reliable
5. **No persistent storage**
   - Orders are processed in-memory
6. **Synchronous flow**
   - User completes ordering before scheduling occurs

These assumptions allow the system to highlight **agent collaboration and MCP usage** without unnecessary complexity.

---

## 3. Handling Ambiguities in User Input

### 3.1 Missing Information

If required details are missing (e.g., size or quantity):

- The Ordering Agent detects incomplete input
- The user is prompted for clarification
- Order placement is deferred until complete information is provided

**Example**:

User: margherita
Bot: Please specify a size (small / medium / large)


---

### 3.2 Quantity Normalization

The system supports multiple quantity formats:

- `x2`, `*2`, `2 margherita`, `margherita x 2`

All formats are normalized internally to:
```json
{
  "pizza": "Margherita",
  "size": "Medium",
  "quantity": 2
}

This ensures consistent downstream processing.

```
---

### 3.3 Invalid Pizza Names or Sizes

If the user enters:

- An unsupported pizza  
- An unavailable size  

The system:

- Validates against the menu MCP  
- Returns a user-friendly error  
- Suggests valid alternatives  

**Example:**
Bot: Pepperoni is not available in Small size.
Available sizes: Medium, Large

---

### 3.4 Partial Agent Failures

If one agent fails (e.g., scheduling agent or calendar MCP):

- Order placement still succeeds  
- A fallback delivery ETA is provided  
- The system does not crash or block the user  

This ensures **graceful degradation**.

---

### 3.5 Ambiguous Natural Language

When user intent is unclear:

- Input is processed incrementally  
- The agent confirms assumptions before action  
- No irreversible operation is executed without clarity  

**Example:**
User: add one more
Bot: Which pizza would you like to add?

---

This system is designed to demonstrate:

- Practical use of MCP for AI-agent tooling  
- Realistic multi-agent collaboration  
- Robust handling of imperfect human input  
- Clean separation between orchestration, tools, and UI

