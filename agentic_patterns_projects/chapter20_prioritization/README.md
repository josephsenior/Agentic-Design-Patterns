# Chapter 20: Prioritization - Task Prioritization System

## Overview

This project implements the **Prioritization Pattern** for managing and ordering tasks based on importance, urgency, and impact.

## Pattern Description

Prioritization enables:
- Task scoring and ranking
- Priority-based task selection
- Multi-criteria evaluation
- Dynamic prioritization

## Features

- Multi-criteria priority scoring
- Automatic task ranking
- Next task selection
- Priority reasoning

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

