# Chapter 13: Human-in-the-Loop - Interactive Agent

## Overview

This project implements the **Human-in-the-Loop Pattern** for scenarios requiring human oversight and escalation.

## Pattern Description

Human-in-the-Loop enables:
- Automatic escalation detection
- Human handoff
- Conversation tracking
- Support workflow management

Sometimes the agent can handle things on its own. Sometimes it needs human help. This pattern knows when to escalate and how to hand off smoothly to a human operator.

## Features

- Escalation decision making (knows when to ask for help)
- Conversation history (keeps track of what was discussed)
- Auto-escalation after N interactions (escalates if it's taking too long)
- Support workflow (smooth handoff to humans)

The agent tries to help first, but if it's stuck or the situation is too complex, it escalates to a human. It keeps the full conversation history so the human knows what's been tried.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from interactive_agent import InteractiveAgent

agent = InteractiveAgent()
result = agent.process_message("I need help with...")
if result["escalated"]:
    print("Transferring to human...")
```

The agent handles what it can, and escalates when it needs to. You can configure when escalation happens - after a certain number of interactions, or when confidence is low, or based on specific triggers.
