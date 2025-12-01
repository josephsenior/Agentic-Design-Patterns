# Chapter 8: Memory Management - Conversation Memory System

## Overview

This project implements the **Memory Management Pattern** for maintaining conversation context and state across interactions.

## Pattern Description

The Memory Management Pattern enables:
- Conversation history retention
- Context awareness
- User preference tracking
- State persistence

## Memory Types

1. **Buffer Memory**: Stores all messages
2. **Summary Memory**: Summarizes conversation over time
3. **Contextual Agent**: Manual context management

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

- Multiple memory types
- Conversation history
- Context extraction
- Memory clearing

