# Document Analysis Pipeline - Prompt Chaining Project

This project demonstrates the **Prompt Chaining** pattern from Agentic Design Patterns in a real-world application. It processes documents through a multi-step pipeline that extracts, analyzes, and structures information.

## Overview

The Document Analysis Pipeline uses prompt chaining to break down complex document processing into sequential steps:

1. **Extraction**: Extract key information from raw text
2. **Entity Identification**: Identify important entities (people, organizations, dates, etc.)
3. **Summary Generation**: Create a concise summary
4. **Structured Output**: Transform everything into a structured JSON format

## Architecture

```
Input Document
    ↓
[Step 1: Extract Information]
    ↓
[Step 2: Identify Entities]
    ↓
[Step 3: Generate Summary]
    ↓
[Step 4: Structure Output]
    ↓
Final JSON Report
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your API key:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage

### Basic Usage

```python
from document_analyzer import DocumentAnalyzer

analyzer = DocumentAnalyzer()
result = analyzer.analyze("Your document text here...")
print(result)
```

### Example

See `example.py` for a complete working example.

## Project Structure

```
chapter1_prompt_chaining/
├── document_analyzer.py    # Main pipeline implementation
├── example.py              # Example usage
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## How Prompt Chaining Works

Each step in the pipeline:
- Receives input from the previous step
- Performs a focused operation
- Passes structured output to the next step
- Can be independently tested and optimized

This modular approach improves reliability and makes the system easier to debug and maintain.

