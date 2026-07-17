"""Validate the minimum contract for every documented pattern example."""

from __future__ import annotations

from pathlib import Path


PATTERN_DIRECTORIES = (
    "prompt_chaining",
    "routing",
    "parallelization",
    "reflection",
    "tool_use",
    "planning",
    "multi_agent",
    "memory",
    "adaptation",
    "mcp",
    "goal_setting",
    "exception_handling",
    "human_in_loop",
    "rag",
    "inter_agent",
    "resource_optimization",
    "reasoning",
    "guardrails",
    "evaluation",
    "prioritization",
    "exploration",
)


def validate_pattern(root: Path, name: str) -> list[str]:
    """Return validation errors for one pattern directory."""
    pattern = root / name
    errors: list[str] = []

    if not pattern.is_dir():
        return [f"{name}: directory is missing"]
    if not (pattern / "README.md").is_file():
        errors.append(f"{name}: README.md is missing")
    if not (pattern / "requirements.txt").is_file():
        errors.append(f"{name}: requirements.txt is missing")
    if not any(pattern.glob("*.py")):
        errors.append(f"{name}: no Python implementation found")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = [
        error
        for name in PATTERN_DIRECTORIES
        for error in validate_pattern(root, name)
    ]

    if len(PATTERN_DIRECTORIES) != 21:
        errors.append("validator must enumerate exactly 21 patterns")
    if not (root / ".env.example").is_file():
        errors.append("root .env.example is missing")

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(PATTERN_DIRECTORIES)} pattern directories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
