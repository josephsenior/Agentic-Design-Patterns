# Chapter 18: Guardrails and Safety - Safety Agent

## Overview

This project implements **Guardrails and Safety Patterns** to validate and filter agent outputs for safety and compliance.

## Pattern Description

Guardrails enable:
- Content safety validation
- Inappropriate content filtering
- Compliance checking
- Safe content generation

Before an agent's output goes out, guardrails check it for safety issues. If something's wrong, they filter it or generate a safe alternative. This is essential for production systems.

## Features

- Safety validation (checks if content is safe)
- Content filtering (removes unsafe parts)
- Safe alternative generation (creates safe versions)
- Guarded agent wrapper (wraps any agent with safety checks)

You can wrap any agent with guardrails, and it'll automatically check outputs before they're returned. If something's unsafe, it either filters it or generates a safe alternative.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from safety_agent import SafetyGuardrail, GuardedAgent

guardrail = SafetyGuardrail()
result = guardrail.validate("Content to check")
if not result["safe"]:
    filtered = guardrail.filter_unsafe("Content")
```

Check content for safety, or wrap an agent so all its outputs are automatically validated. This is crucial when building systems that interact with users or handle sensitive information.
