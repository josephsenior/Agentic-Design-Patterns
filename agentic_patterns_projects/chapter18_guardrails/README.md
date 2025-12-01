# Chapter 18: Guardrails and Safety - Safety Agent

## Overview

This project implements **Guardrails and Safety Patterns** to validate and filter agent outputs for safety and compliance.

## Pattern Description

Guardrails enable:
- Content safety validation
- Inappropriate content filtering
- Compliance checking
- Safe content generation

## Features

- Safety validation
- Content filtering
- Safe alternative generation
- Guarded agent wrapper

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

