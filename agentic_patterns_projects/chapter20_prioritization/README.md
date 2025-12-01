# Chapter 20: Prioritization - Task Prioritization System

## Overview

This project implements the **Prioritization Pattern** for managing and ordering tasks based on importance, urgency, and impact.

## Pattern Description

Prioritization enables:
- Task scoring and ranking
- Priority-based task selection
- Multi-criteria evaluation
- Dynamic prioritization

Not all tasks are created equal. This pattern helps you figure out what to do first by scoring tasks on multiple criteria and ranking them automatically.

## Features

- Multi-criteria priority scoring (considers importance, urgency, impact, etc.)
- Automatic task ranking (orders tasks by priority)
- Next task selection (tells you what to do next)
- Priority reasoning (explains why something is prioritized)

Add tasks with context, and the system scores them and ranks them. Ask what to do next, and it'll tell you the highest priority task and why it's important.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from priority_manager import PriorityManager

manager = PriorityManager()
task = manager.add_task("Your task", "Context")
prioritized = manager.get_prioritized_tasks()
next_task = manager.get_next_task()
```

Add tasks, and they're automatically prioritized. Get the full ranked list, or just ask what to do next. The system considers multiple factors to figure out what's most important.

This is really useful when you have lots of tasks and need to focus on what matters most. The prioritization adapts as you add more tasks or complete existing ones.
