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

Think of tools as superpowers for your agent. The LLM can reason and generate text, but tools let it actually do things like search the web, calculate math, or check the current time.

## Available Tools

1. **search_information**: Search for factual information
2. **calculate**: Perform mathematical calculations
3. **get_current_time**: Get current date and time
4. **word_count**: Analyze text statistics

You can easily add more tools by creating new functions and registering them with the agent. The agent will automatically decide when to use which tool based on what you're asking.

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

- Automatic tool selection (the agent picks the right tool)
- Tool result integration (seamlessly combines tool outputs with reasoning)
- Error handling (gracefully handles tool failures)
- Async support (for better performance)

The agent is smart about when to use tools. Ask it a math question and it'll use the calculator. Ask about facts and it'll search. It figures this out on its own.
