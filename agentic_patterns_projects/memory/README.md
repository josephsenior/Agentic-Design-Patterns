# Chapter 8: Memory Management - Conversation Memory System

## Overview

This project implements the **Memory Management Pattern** for maintaining conversation context and state across interactions.

## Pattern Description

The Memory Management Pattern enables:
- Conversation history retention
- Context awareness
- User preference tracking
- State persistence

This is what makes conversations feel natural. Without memory, every interaction starts from scratch. With memory, the agent remembers what you talked about before, what you like, and the context of your conversation.

## Memory Types

1. **Buffer Memory**: Stores all messages (simple but can get long)
2. **Summary Memory**: Summarizes conversation over time (more efficient)
3. **Contextual Agent**: Manual context management (most control)

Each type has trade-offs. Buffer memory is simple but can get expensive with long conversations. Summary memory is more efficient but might lose some details. The contextual agent gives you the most control but requires more setup.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from memory_system import ConversationMemory

memory = ConversationMemory(memory_type="buffer")
result = memory.chat("Hello, my name is Alice")
result = memory.chat("What's my name?")  # Remembers!
```

## Features

- Multiple memory types (choose what works for your use case)
- Conversation history (see what was said before)
- Context extraction (pull out important information)
- Memory clearing (start fresh when needed)

The agent remembers your name, your preferences, and the context of your conversation. Ask it what you talked about earlier, and it'll know. This makes interactions feel much more natural and useful.
