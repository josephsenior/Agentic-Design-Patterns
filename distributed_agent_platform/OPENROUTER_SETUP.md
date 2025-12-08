# OpenRouter Setup Guide

This guide explains how to use OpenRouter's free models as an alternative to OpenAI for demos.

## Quick Setup

### 1. Add OpenRouter API Key to `.env`

```env
# Existing OpenAI config (keep this)
OPENAI_API_KEY=your_openai_key_here

# OpenRouter config (add these)
USE_OPENROUTER=true
OPENROUTER_API_KEY=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
OPENROUTER_MODEL=tngtech/deepseek-r1t2-chimera:free
```

### 2. Enable OpenRouter

Set `USE_OPENROUTER=true` in your `.env` file to use OpenRouter instead of OpenAI.

### 3. Restart the Application

The application will automatically use OpenRouter when `USE_OPENROUTER=true` is set.

## Available Free Models

### Recommended: DeepSeek R1T2 Chimera
- **Model ID**: `tngtech/deepseek-r1t2-chimera:free`
- **Best for**: General purpose, reasoning tasks, distributed agents
- **Context**: Large context window
- **Free**: Yes

### Alternative Models

You can change `OPENROUTER_MODEL` to any of these:

- `meta-llama/llama-4-scout:free` - Large model, 512K context
- `mistralai/mistral-7b-instruct:free` - Fast, 7B parameters
- `qwen/qwen-2.5-7b-instruct:free` - Balanced performance

## Usage

The system automatically detects `USE_OPENROUTER` and switches between OpenAI and OpenRouter. All distributed agents (Researcher, Analyst, Coordinator, Knowledge) will use the configured provider. No code changes needed!

**Note**: This project uses AutoGen, which is configured to work with OpenRouter through the base URL configuration.

## Switching Between Providers

Simply change `USE_OPENROUTER` in your `.env` file:

```env
# Use OpenAI
USE_OPENROUTER=false

# Use OpenRouter
USE_OPENROUTER=true
```

## API Key

Your OpenRouter API key:
```
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
```

Keep this secure and don't commit it to version control.

