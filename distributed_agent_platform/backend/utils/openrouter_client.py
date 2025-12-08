"""OpenRouter client utility for using free models as an alternative to OpenAI."""

import os
from typing import Optional
from langchain_openai import ChatOpenAI


def create_llm(
    model_name: str = "gpt-4",
    temperature: float = 0.7,
    api_key: Optional[str] = None
) -> ChatOpenAI:
    """Create LLM instance with support for OpenAI or OpenRouter.
    
    Args:
        model_name: Model name (OpenAI model or OpenRouter model)
        temperature: Sampling temperature
        api_key: API key (defaults to env vars)
        
    Returns:
        ChatOpenAI instance configured for OpenAI or OpenRouter
    """
    use_openrouter = os.getenv("USE_OPENROUTER", "false").lower() == "true"
    
    if use_openrouter:
        # Use OpenRouter
        openrouter_key = api_key or os.getenv("OPENROUTER_API_KEY")
        openrouter_model = os.getenv("OPENROUTER_MODEL", "tngtech/deepseek-r1t2-chimera:free")
        
        if not openrouter_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required when USE_OPENROUTER=true")
        
        return ChatOpenAI(
            model=openrouter_model,
            temperature=temperature,
            api_key=openrouter_key,
            openai_api_base="https://openrouter.ai/api/v1",
        )
    else:
        # Use OpenAI (default)
        openai_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not openai_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=openai_key,
        )

