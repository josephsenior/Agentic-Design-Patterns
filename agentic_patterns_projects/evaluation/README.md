# Chapter 19: Evaluation and Monitoring - Agent Evaluation System

## Overview

This project implements the **Evaluation and Monitoring Pattern** using LLM-as-a-Judge to assess agent performance.

## Pattern Description

Evaluation enables:
- Response quality assessment
- Multi-criteria evaluation
- Performance monitoring
- Response comparison

How do you know if your agent is doing a good job? This pattern uses another LLM to evaluate responses across multiple criteria, giving you objective quality scores.

## Evaluation Criteria

- Correctness (is the answer right?)
- Relevance (does it address the question?)
- Completeness (does it cover everything?)
- Clarity (is it easy to understand?)
- Helpfulness (is it actually useful?)

The evaluator scores responses on all these dimensions, so you can see where your agent excels and where it needs improvement.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from evaluation_system import AgentEvaluator

evaluator = AgentEvaluator()
result = evaluator.evaluate("Question", "Agent response")
print(result["scores"])
```

Give it a question and the agent's response, and it'll score the response across all criteria. Use this to monitor performance over time or compare different approaches.

This is really useful for improving your agents. You can test different prompts or configurations and see which ones score higher.
