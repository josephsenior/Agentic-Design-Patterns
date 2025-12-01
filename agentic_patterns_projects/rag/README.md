# Chapter 14: Knowledge Retrieval (RAG) - RAG System

## Overview

This project implements the **Retrieval-Augmented Generation (RAG) Pattern** that combines document retrieval with LLM generation for accurate, context-aware responses.

## Pattern Description

RAG enables:
- Document-based knowledge retrieval
- Context-aware responses
- Accurate information from knowledge base
- Scalable knowledge management

Instead of relying only on what the LLM knows, RAG lets you give it access to your own documents. It finds relevant information from your knowledge base and uses that to generate accurate, context-aware answers.

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

First, it searches your documents to find relevant information. Then it uses that information along with the question to generate an answer. This means the answers are grounded in your actual data, not just general knowledge.

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

Load your documents, ask questions, and get answers based on what's actually in your documents. You can add more documents anytime, and the system will use them for future queries.

## Features

- Vector-based retrieval (finds relevant documents quickly)
- Document chunking (handles long documents efficiently)
- Context-aware generation (uses retrieved info in answers)
- Extensible knowledge base (add documents as you go)

The system uses vector embeddings to find the most relevant parts of your documents, then includes that context when generating answers. This makes responses much more accurate and specific to your data.
