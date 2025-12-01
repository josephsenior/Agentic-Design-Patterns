# Chapter 2: Routing Pattern - Smart Request Router

## Overview

This project implements the **Routing Pattern** to intelligently direct user requests to specialized handlers based on the request type. It demonstrates how to use LangChain's `RunnableBranch` to create a coordinator that routes requests to appropriate sub-agents.

## Pattern Description

The Routing Pattern allows a coordinator agent to analyze incoming requests and delegate them to specialized handlers. This is useful for:
- Customer support systems
- Multi-domain assistants
- Request classification and routing

## Architecture

```
User Request
    ↓
[Coordinator Router]
    ↓
    ├─→ [Booking Handler] (for booking requests)
    ├─→ [Info Handler] (for information requests)
    └─→ [Unclear Handler] (for ambiguous requests)
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from smart_router import SmartRouter

router = SmartRouter()
result = router.route("Book me a flight to Paris")
print(result)
```

## Example Use Cases

- **Booking Requests**: "Book a hotel room", "Reserve a table"
- **Information Requests**: "What is the weather?", "Tell me about..."
- **Unclear Requests**: Handled with clarification prompts

