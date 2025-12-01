# Chapter 14: Knowledge Retrieval (RAG) - RAG System

## Overview

This project implements the **Retrieval-Augmented Generation (RAG) Pattern** that combines document retrieval with LLM generation for accurate, context-aware responses.

## Pattern Description

RAG enables:
- Document-based knowledge retrieval
- Context-aware responses
- Accurate information from knowledge base
- Scalable knowledge management

## Architecture

```
Question
    ↓
[Retrieve] → Relevant Documents
    ↓
[Generate] → Context + Question
    ↓
Answer
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from rag_system import RAGSystem

rag = RAGSystem()
rag.load_documents(["Document 1...", "Document 2..."])
result = rag.query("Your question here")
print(result["answer"])
```

## Features

- Vector-based retrieval
- Document chunking
- Context-aware generation
- Extensible knowledge base

