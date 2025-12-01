# Chapter 15: Inter-Agent Communication - Agent Communication System

## Overview

This project implements the **Inter-Agent Communication Pattern** for agents to communicate and collaborate with each other.

## Pattern Description

Inter-agent communication enables:
- Message passing between agents
- Request-response patterns
- Broadcast messaging
- Agent coordination

When you have multiple agents, they need to talk to each other. This pattern provides a communication system so agents can send messages, make requests, and coordinate their work.

## Features

- Message routing (messages go to the right agent)
- Agent registration (agents can join the network)
- Request-response handling (agents can ask each other for help)
- Broadcast capabilities (send messages to everyone)

Agents register with a communication hub, and then they can send messages to each other. One agent can ask another for help, or broadcast a message to everyone.

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

Agents register with the hub, and then they can communicate. Send a message from one agent to another, or broadcast to all agents. This makes it easy to build systems where agents collaborate.
