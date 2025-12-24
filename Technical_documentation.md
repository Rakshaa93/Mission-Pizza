# Technical Documentation  
## Pizza AI Agent System

---

### 1.Problem Understanding
The core problem is not pizza ordering, but making traditional APIs usable by AI agents.

Key Challenges Identified:

-REST APIs are not agent-friendly
-Manual MCP creation does not scale
-AI agents require:
   *Structured tools
   *Clear schemas
   *Predictable behavior
-Real-world workflows require multi-agent coordination

Hence, the solution focuses on:

-Automated OpenAPI → MCP translation
-Agent-to-Agent (A2A) workflows
-Graceful handling of ambiguity and partial failures

---
### 2.System Architecture Overview
The system is composed of four logical layers:

#### 2.1 Specification Layer

Input: OpenAPI YAML/JSON
Responsibility:
-Parse endpoints
-Extract request/response schemas
-Generate MCP tool definitions

#### 2.2 MCP Server Layer
Auto-generated MCP server exposes:
-get_menu
-place_order
-track_order

Acts as the single source of truth for pizza operations
Mocked backend data is used intentionally, as allowed by the problem statement 

#### 2.3 Agent Layer

Ordering Agent

Handles natural language input

Calls MCP tools

Maintains order state

Scheduling Agent

Receives order details via A2A

Uses an external MCP (calendar mock)

Performs delivery coordination

3.4 Interface Layer

Lightweight web chat UI

Used only for demonstration

Not a core evaluation component

