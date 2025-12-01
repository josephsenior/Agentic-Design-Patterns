# Chapter 15: Inter-Agent Communication - Agent Communication System

## Overview

This project implements the **Inter-Agent Communication Pattern** for agents to communicate and collaborate with each other.

## Pattern Description

Inter-agent communication enables:
- Message passing between agents
- Request-response patterns
- Broadcast messaging
- Agent coordination

## Features

- Message routing
- Agent registration
- Request-response handling
- Broadcast capabilities

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from agent_communication import CommunicatingAgent, AgentCommunicationHub

hub = AgentCommunicationHub()
hub.register_agent(agent1)
hub.register_agent(agent2)
result = hub.send_message("agent1", "agent2", "Message content")
```

