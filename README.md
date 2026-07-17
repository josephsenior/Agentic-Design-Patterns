# Agentic Design Patterns

> 21 runnable reference implementations for understanding common LLM-agent workflow patterns.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/josephsenior/Agentic-Design-Patterns/actions/workflows/ci.yml/badge.svg)](https://github.com/josephsenior/Agentic-Design-Patterns/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/josephsenior/Agentic-Design-Patterns)](https://github.com/josephsenior/Agentic-Design-Patterns/stargazers)
[![Issues](https://img.shields.io/github/issues/josephsenior/Agentic-Design-Patterns)](https://github.com/josephsenior/Agentic-Design-Patterns/issues)

This repository is a clean-room educational reference library containing runnable implementations of 21 agent design primitives. Each directory isolates one pattern and pairs the implementation with a small practical example.

The goal is not to present one universal agent framework. It is to make individual orchestration ideas easy to inspect, run, compare, and combine.

> **Project status:** educational reference implementations. CI verifies repository structure and Python syntax; examples that call external model APIs are not treated as production systems or exercised end to end without credentials.

## Patterns

| # | Pattern | Reference use case |
|---|---|---|
| 1 | Prompt Chaining | Sequential document processing |
| 2 | Routing | Request classification and delegation |
| 3 | Parallelization | Concurrent analysis and synthesis |
| 4 | Reflection | Generate, critique, refine |
| 5 | Tool Use | Function calling and external tools |
| 6 | Planning | Goal decomposition and task execution |
| 7 | Multi-Agent | Specialized agent collaboration |
| 8 | Memory | Conversation state and persistence |
| 9 | Adaptation | Feedback-driven behavior changes |
| 10 | MCP | Standardized tool/resource integration |
| 11 | Goal Setting | Goal breakdown and progress tracking |
| 12 | Exception Handling | Fallback and recovery workflows |
| 13 | Human-in-the-Loop | Escalation and human feedback |
| 14 | RAG | Retrieval-augmented generation |
| 15 | Inter-Agent Communication | Agent-to-agent messaging |
| 16 | Resource Optimization | Caching, batching, and cost control |
| 17 | Reasoning | Structured problem-solving workflows |
| 18 | Guardrails | Validation and policy checks |
| 19 | Evaluation | LLM-as-a-Judge and quality assessment |
| 20 | Prioritization | Priority-based task ordering |
| 21 | Exploration | Testing multiple candidate approaches |

## Quick start

Clone the repository:

```bash
git clone https://github.com/josephsenior/Agentic-Design-Patterns.git
cd Agentic-Design-Patterns
cp .env.example .env
```

Move into a pattern directory, install its dependencies, and run the example:

```bash
cd prompt_chaining
pip install -r requirements.txt
python example.py
```

Some examples use Gemini. Add the required API key to the pattern's `.env` file when needed.

## Repository philosophy

Each implementation is intentionally small and pattern-focused:

```text
pattern_name/
├── implementation.py
├── example.py
├── README.md
├── requirements.txt
└── .env.example
```

Exact filenames can vary by pattern, but the examples are organized so the orchestration primitive remains easy to identify.

## How the patterns relate

### Sequential and planning

- Prompt Chaining
- Planning
- Goal Setting
- Prioritization

These patterns organize work over time and make task progression explicit.

### Decision and feedback

- Routing
- Reflection
- Adaptation
- Exploration

These patterns select, critique, revise, or compare candidate paths.

### Tools and coordination

- Tool Use
- Multi-Agent
- Inter-Agent Communication
- MCP

These patterns connect agents to capabilities or to other specialized agents.

### State and knowledge

- Memory
- RAG

These patterns provide persistent conversational state or external knowledge retrieval.

### Reliability and control

- Exception Handling
- Human-in-the-Loop
- Guardrails
- Evaluation
- Resource Optimization

These patterns help make agent workflows more observable, bounded, and testable.

## Example combinations

| Combination | Use case |
|---|---|
| Routing + Tool Use | Select the right capability for each request |
| Planning + Evaluation | Validate progress before advancing |
| RAG + Tool Use | Combine retrieved context with external actions |
| Memory + Adaptation | Use historical feedback to adjust behavior |
| Multi-Agent + Inter-Agent Communication | Coordinate specialized roles |
| Guardrails + Exception Handling | Bound actions and recover from failures |

## Who this is for

- Engineers learning agent orchestration beyond single-prompt applications
- Students comparing common LLM-agent patterns
- Builders looking for small references before integrating a pattern into a larger system

For a larger autonomous-agent runtime that combines planning, tools, execution, durability, and validation, see [Grinta](https://github.com/josephsenior/Grinta-Coding-Agent).

## Contributing

Issues and pull requests are welcome.

- [Open an issue](https://github.com/josephsenior/Agentic-Design-Patterns/issues)
- [View the repository](https://github.com/josephsenior/Agentic-Design-Patterns)

## License

MIT — see [LICENSE](LICENSE).
