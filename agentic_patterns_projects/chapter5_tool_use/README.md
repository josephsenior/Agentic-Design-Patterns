# Chapter 5: Tool Use Pattern - Research Assistant with Tools

## Overview

This project implements the **Tool Use Pattern** where an agent can call external tools to extend its capabilities beyond what the LLM can do directly.

## Pattern Description

The Tool Use Pattern enables agents to:
- Search for information
- Perform calculations
- Access external APIs
- Execute code
- Interact with databases

## Available Tools

1. **search_information**: Search for factual information
2. **calculate**: Perform mathematical calculations
3. **get_current_time**: Get current date and time
4. **word_count**: Analyze text statistics

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from research_assistant import ResearchAssistant

assistant = ResearchAssistant()
result = assistant.ask("What is the capital of France?")
print(result["answer"])
```

## Features

- Automatic tool selection
- Tool result integration
- Error handling
- Async support

