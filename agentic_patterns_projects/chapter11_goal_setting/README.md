# Chapter 11: Goal Setting and Monitoring - Goal-Oriented Agent

## Overview

This project implements the **Goal Setting and Monitoring Pattern** for agents that work towards specific objectives with progress tracking.

## Pattern Description

Goal setting enables:
- Goal breakdown into sub-goals
- Progress tracking
- Status monitoring
- Iterative goal achievement

## Features

- SMART goal breakdown
- Progress assessment
- Action tracking
- Status monitoring

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from goal_agent import GoalAgent

agent = GoalAgent()
goal = agent.set_goal("Your goal here")
agent.update_progress(goal["id"], "Completed action")
```

