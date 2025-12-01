# Chapter 6: Planning Pattern - Task Planning System

## Overview

This project implements the **Planning Pattern** where an agent breaks down complex goals into actionable, sequential tasks and executes them step by step.

## Pattern Description

The Planning Pattern enables:
- Goal decomposition
- Task sequencing
- Dependency management
- Step-by-step execution

## Architecture

```
Goal
    ↓
[Create Plan] → Structured Tasks
    ↓
[Execute Tasks] → Step 1 → Step 2 → Step 3 → ...
    ↓
Final Result
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from task_planner import TaskPlanner

planner = TaskPlanner()
result = planner.plan_and_execute("Your goal here", execute=True)
```

## Features

- Automatic plan generation
- Task dependency tracking
- Sequential execution
- Execution results tracking

