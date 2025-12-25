"""Offline checks that keep every example importable and documented."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", ".venv", "__pycache__", "tests"}


def source_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*.py")
        if not any(part in EXCLUDED_PARTS for part in path.parts)
    ]


def test_examples_parse_without_syntax_errors() -> None:
    files = source_files()
    assert len(files) >= 21
    for path in files:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_each_pattern_has_a_readme_and_requirements() -> None:
    pattern_directories = [path.parent for path in source_files()]
    for directory in pattern_directories:
        assert (directory / "README.md").is_file()
        assert (directory / "requirements.txt").is_file()


def test_examples_use_the_documented_google_integration() -> None:
    for path in source_files():
        source = path.read_text(encoding="utf-8")
        if "langchain_google_genai" in source:
            assert "ChatGemini" not in source
            assert "langchain_Gemini" not in source
            assert "gpt-3.5-turbo" not in source
