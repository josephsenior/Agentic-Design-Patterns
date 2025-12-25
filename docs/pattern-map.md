# Agentic design-pattern map

Use this map to choose a starting point. Patterns are intentionally small and composable: begin with one need, then follow the suggested combinations.

```mermaid
flowchart LR
    A[Your agent] --> B{Primary need}
    B --> C[Orchestration\nPrompt Chaining · Planning · Routing]
    B --> D[Collaboration\nParallelization · Multi-Agent · MCP]
    B --> E[Knowledge & state\nMemory · RAG · Goal Setting]
    B --> F[Quality & safety\nReflection · Guardrails · Evaluation]
    B --> G[Resilience & efficiency\nException Handling · Resource Optimization]
    C --> H[Production workflow]
    D --> H
    E --> H
    F --> H
    G --> H
```

## Recommended combinations

| Goal | Start with | Add next |
| --- | --- | --- |
| Build a trustworthy knowledge assistant | RAG | Guardrails, Evaluation, Memory |
| Automate multi-step work | Prompt Chaining | Planning, Exception Handling |
| Serve varied user requests | Routing | Tool Use, Human-in-the-Loop |
| Coordinate specialist agents | Multi-Agent | Inter-Agent Communication, Evaluation |

Each pattern directory contains its implementation and a focused explanation. The examples are learning-oriented reference implementations; validate security, evaluation criteria, costs, and provider limits before deploying them in production.
