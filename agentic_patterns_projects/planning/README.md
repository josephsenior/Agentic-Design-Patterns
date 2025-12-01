# Chapter 6: Planning Pattern - Task Planning System

## Overview

This project implements the **Planning Pattern** where an agent breaks down complex goals into actionable, sequential tasks and executes them step by step.

## Pattern Description

The Planning Pattern enables:
- Goal decomposition
- Task sequencing
- Dependency management
- Step-by-step execution

This is like having a project manager that takes your big, vague goal and turns it into a clear step-by-step plan. Then it can execute that plan for you, checking off tasks as it goes.

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

- Automatic plan generation (breaks down goals intelligently)
- Task dependency tracking (knows what needs to happen first)
- Sequential execution (runs tasks in the right order)
- Execution results tracking (keeps track of what's done)

You can use it just to create a plan, or you can have it execute the plan automatically. The planner understands dependencies, so if task 3 depends on task 1, it'll make sure task 1 happens first.
