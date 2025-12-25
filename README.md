# Agentic Design Patterns — runnable Python references

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Verify examples](https://github.com/josephsenior/Agentic-design-patterns-/actions/workflows/verify.yml/badge.svg)](https://github.com/josephsenior/Agentic-design-patterns-/actions/workflows/verify.yml)
[![Stars](https://img.shields.io/github/stars/josephsenior/Agentic-design-patterns-?style=social)](https://github.com/josephsenior/Agentic-design-patterns-/stargazers)

Learn how to assemble AI agents from 21 focused, runnable design-pattern examples. Every directory pairs one pattern with a small real-world scenario, making it easy to learn a technique in isolation and then combine it with others.

> These are educational reference implementations—not turnkey production services. Before deploying, add application-specific authentication, observability, evaluation, cost controls, and security review.

## Start here

```bash
git clone https://github.com/josephsenior/Agentic-design-patterns-.git
cd Agentic-design-patterns-
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# Put your Google AI Studio key in .env, then choose a pattern.
cp .env.example .env
cd prompt_chaining
python example.py
```

On Windows, use `Copy-Item .env.example .env` rather than `cp` if preferred. Pattern-specific dependencies are documented in each `requirements.txt`; for RAG, install `rag/requirements.txt` as well.

## Choose a pattern

| Need | Patterns |
| --- | --- |
| Build multi-step workflows | Prompt Chaining, Planning, Routing, Prioritization |
| Coordinate concurrent or specialist work | Parallelization, Multi-Agent, Inter-Agent Communication, MCP |
| Retain or retrieve context | Memory, RAG, Goal Setting |
| Improve quality and safety | Reflection, Guardrails, Evaluation, Human-in-the-Loop |
| Make agents more robust | Adaptation, Exception Handling, Resource Optimization, Exploration, Reasoning, Tool Use |

See the [visual pattern map](docs/pattern-map.md) for combinations and suggested starting points.

## All examples

| # | Pattern | Scenario |
| --- | --- | --- |
| 1 | [Prompt Chaining](prompt_chaining/) | Document analysis pipeline |
| 2 | [Routing](routing/) | Smart request router |
| 3 | [Parallelization](parallelization/) | Parallel document processor |
| 4 | [Reflection](reflection/) | Self-improving content generator |
| 5 | [Tool Use](tool_use/) | Research assistant |
| 6 | [Planning](planning/) | Task planning system |
| 7 | [Multi-Agent](multi_agent/) | Collaborative team |
| 8 | [Memory](memory/) | Conversation memory |
| 9 | [Adaptation](adaptation/) | Feedback-driven agent |
| 10 | [MCP](mcp/) | Model Context Protocol integration |
| 11 | [Goal Setting](goal_setting/) | Goal-oriented agent |
| 12 | [Exception Handling](exception_handling/) | Error recovery and fallback |
| 13 | [Human-in-the-Loop](human_in_loop/) | Escalation workflow |
| 14 | [RAG](rag/) | Knowledge retrieval |
| 15 | [Inter-Agent Communication](inter_agent/) | Agent messaging |
| 16 | [Resource Optimization](resource_optimization/) | Caching and batching |
| 17 | [Reasoning](reasoning/) | Structured problem solving |
| 18 | [Guardrails](guardrails/) | Content validation |
| 19 | [Evaluation](evaluation/) | LLM-as-a-judge |
| 20 | [Prioritization](prioritization/) | Priority-based task management |
| 21 | [Exploration](exploration/) | Experimental discovery |

## Learning paths

- **First agent:** Prompt Chaining → Routing → Tool Use → Memory.
- **Reliable knowledge assistant:** RAG → Guardrails → Evaluation → Human-in-the-Loop.
- **Agent team:** Planning → Parallelization → Multi-Agent → Inter-Agent Communication.

## Verification

Run the repository checks locally before opening a pull request:

```bash
python -m pytest
```

Continuous integration performs the same offline checks on every pull request and push to `main`. Live model calls are deliberately excluded from CI because they require credentials and incur cost.

## Contributing

Contributions are welcome—new scenarios, clearer documentation, tests, and provider-neutral improvements are especially useful. Please read [CONTRIBUTING.md](CONTRIBUTING.md), use the issue templates, and keep each pattern self-contained.

## GitHub discoverability checklist

After pushing, configure the repository’s GitHub **About** section with a short description, this repository’s website/docs link if available, and topics such as `ai-agents`, `agentic-ai`, `llm`, `langchain`, `gemini`, `rag`, `mcp`, `multi-agent`, `python`, and `design-patterns`. Add a social-preview image and enable Discussions to help prospective users find and evaluate the project.

## License

MIT — see [LICENSE](LICENSE).
