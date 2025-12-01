# Chapter 11: Goal Setting and Monitoring - Goal-Oriented Agent

## Overview

This project implements the **Goal Setting and Monitoring Pattern** for agents that work towards specific objectives with progress tracking.

## Pattern Description

Goal setting enables:
- Goal breakdown into sub-goals
- Progress tracking
- Status monitoring
- Iterative goal achievement

This is like having an agent that doesn't just do tasks, but actually works toward goals. It breaks big goals into smaller pieces, tracks progress, and knows when it's getting closer to completion.

## Features

- SMART goal breakdown (Specific, Measurable, Achievable, Relevant, Time-bound)
- Progress assessment (knows how far along it is)
- Action tracking (remembers what's been done)
- Status monitoring (can check in on progress anytime)

You set a goal, and the agent figures out what needs to happen to achieve it. Then it tracks progress as it works, so you always know where things stand.

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

Set a goal, and the agent will break it down and track progress. You can check in anytime to see how things are going and what still needs to be done.
