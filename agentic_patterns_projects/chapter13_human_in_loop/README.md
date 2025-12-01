# Chapter 13: Human-in-the-Loop - Interactive Agent

## Overview

This project implements the **Human-in-the-Loop Pattern** for scenarios requiring human oversight and escalation.

## Pattern Description

Human-in-the-Loop enables:
- Automatic escalation detection
- Human handoff
- Conversation tracking
- Support workflow management

## Features

- Escalation decision making
- Conversation history
- Auto-escalation after N interactions
- Support workflow

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

