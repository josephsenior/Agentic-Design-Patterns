"""
Resource-Aware Optimization - Resource-Aware Optimization Pattern

This module implements resource optimization strategies for efficient
API usage, token management, and cost optimization.
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from functools import lru_cache
import time

load_dotenv()


class ResourceOptimizer:
    """
    A system for optimizing resource usage in agent operations.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0,
        api_key: Optional[str] = None
    ):
        """Initialize the Resource Optimizer."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self.call_count = 0
        self.total_tokens = 0
        self.cache = {}
        self._build_optimized_chain()
    
    def _build_optimized_chain(self):
        """Build optimized chains with caching."""
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Provide concise, accurate responses."),
            ("user", "{query}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    @lru_cache(maxsize=100)
    def cached_query(self, query: str) -> str:
        """
        Query with caching to avoid redundant API calls.
        
        Args:
            query: The query string
            
        Returns:
            Response from cache or LLM
        """
        if query in self.cache:
            print(f"💾 Cache hit for: {query[:50]}...")
            return self.cache[query]
        
        print(f"🌐 API call for: {query[:50]}...")
        self.call_count += 1
        response = self.chain.invoke({"query": query})
        self.cache[query] = response
        return response
    
    def batch_process(self, queries: List[str]) -> List[str]:
        """
        Process multiple queries efficiently.
        
        Args:
            queries: List of queries
            
        Returns:
            List of responses
        """
        # Deduplicate queries
        unique_queries = list(set(queries))
        
        # Process unique queries
        results = {}
        for query in unique_queries:
            results[query] = self.cached_query(query)
        
        # Return results in original order
        return [results[q] for q in queries]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get resource usage statistics."""
        return {
            "api_calls": self.call_count,
            "cache_size": len(self.cache),
            "cache_hits": self.call_count - len(self.cache),
            "total_queries_processed": self.call_count + len(self.cache)
        }
    
    def clear_cache(self):
        """Clear the cache."""
        self.cache.clear()
        self.cached_query.cache_clear()
        print("🧹 Cache cleared")


class TokenOptimizer:
    """
    Optimizes token usage in prompts and responses.
    """
    
    def __init__(self, llm):
        self.llm = llm
    
    def optimize_prompt(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Optimize a prompt to reduce token usage.
        
        Args:
            prompt: Original prompt
            max_tokens: Maximum token limit
            
        Returns:
            Optimized prompt
        """
        optimization_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a prompt optimizer. Make this prompt more concise while preserving its meaning and intent."),
            ("user", f"Optimize this prompt to use fewer tokens:\n\n{prompt}")
        ])
        
        chain = optimization_prompt | self.llm | StrOutputParser()
        optimized = chain.invoke({"prompt": prompt})
        return optimized


if __name__ == "__main__":
    optimizer = ResourceOptimizer()
    
    print("=" * 70)
    print("RESOURCE OPTIMIZER - RESOURCE-AWARE OPTIMIZATION")
    print("=" * 70)
    
    # Test caching
    queries = [
        "What is Python?",
        "What is Python?",  # Duplicate - should use cache
        "What is JavaScript?",
        "What is Python?",  # Another duplicate
    ]
    
    print("\nProcessing queries with caching...")
    for query in queries:
        result = optimizer.cached_query(query)
        print(f"   Query: {query}")
        print(f"   Response: {result[:50]}...")
    
    print("\n" + "=" * 70)
    print("STATISTICS")
    print("=" * 70)
    stats = optimizer.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")

