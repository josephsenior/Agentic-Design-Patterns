"""
Robust Agent with Fallback - Exception Handling and Recovery Pattern

This module implements exception handling and recovery strategies for robust agent behavior.
"""

import os
from typing import Dict, Any, Optional, Callable
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class RobustAgent:
    """
    An agent with exception handling and fallback mechanisms.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0,
        api_key: Optional[str] = None
    ):
        """Initialize the Robust Agent."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self._build_handlers()
    
    def _build_handlers(self):
        """Build primary and fallback handlers."""
        
        # Primary handler
        self.primary_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant. Try to answer the user's question 
directly and accurately. If you encounter any issues, indicate them clearly."""),
            ("user", "{query}")
        ])
        
        self.primary_chain = self.primary_prompt | self.llm | StrOutputParser()
        
        # Fallback handler
        self.fallback_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a fallback assistant. The primary handler encountered 
an issue. Provide a helpful response using general knowledge or ask for clarification."""),
            ("user", """Original query: {query}
Error context: {error_context}
Provide a helpful fallback response.""")
        ])
        
        self.fallback_chain = self.fallback_prompt | self.llm | StrOutputParser()
    
    def process_with_fallback(
        self,
        query: str,
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """
        Process a query with fallback handling.
        
        Args:
            query: The user's query
            max_retries: Maximum retry attempts
            
        Returns:
            Dictionary with result and execution details
        """
        result = {
            "query": query,
            "success": False,
            "response": None,
            "method": None,
            "errors": []
        }
        
        # Try primary handler
        for attempt in range(max_retries):
            try:
                response = self.primary_chain.invoke({"query": query})
                result["success"] = True
                result["response"] = response
                result["method"] = "primary"
                return result
            except Exception as e:
                error_msg = f"Attempt {attempt + 1} failed: {str(e)}"
                result["errors"].append(error_msg)
                print(f"⚠️  {error_msg}")
        
        # Fallback handler
        try:
            error_context = "; ".join(result["errors"])
            response = self.fallback_chain.invoke({
                "query": query,
                "error_context": error_context
            })
            result["success"] = True
            result["response"] = response
            result["method"] = "fallback"
            return result
        except Exception as e:
            result["errors"].append(f"Fallback failed: {str(e)}")
            result["response"] = "I apologize, but I'm unable to process your request at this time. Please try again later."
            return result


class ResilientToolAgent:
    """
    An agent that handles tool failures gracefully.
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.tool_failures = []
    
    def safe_tool_call(self, tool_func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Safely call a tool with error handling.
        
        Args:
            tool_func: The tool function to call
            *args, **kwargs: Arguments for the tool
            
        Returns:
            Dictionary with result or error
        """
        try:
            result = tool_func(*args, **kwargs)
            return {
                "success": True,
                "result": result,
                "error": None
            }
        except Exception as e:
            error_info = {
                "tool": tool_func.__name__,
                "error": str(e),
                "args": args,
                "kwargs": kwargs
            }
            self.tool_failures.append(error_info)
            
            return {
                "success": False,
                "result": None,
                "error": str(e),
                "error_info": error_info
            }
    
    def get_failure_summary(self) -> str:
        """Get a summary of tool failures."""
        if not self.tool_failures:
            return "No tool failures recorded."
        
        summary = f"Total failures: {len(self.tool_failures)}\n"
        for failure in self.tool_failures:
            summary += f"- {failure['tool']}: {failure['error']}\n"
        return summary


if __name__ == "__main__":
    agent = RobustAgent()
    
    print("=" * 70)
    print("ROBUST AGENT - EXCEPTION HANDLING AND RECOVERY")
    print("=" * 70)
    
    queries = [
        "What is the capital of France?",
        "Calculate 2 + 2",
        "Tell me about artificial intelligence"
    ]
    
    for query in queries:
        print(f"\n📥 Query: {query}")
        result = agent.process_with_fallback(query)
        print(f"✅ Success: {result['success']}")
        print(f"🔧 Method: {result['method']}")
        print(f"💬 Response: {result['response']}")
        if result['errors']:
            print(f"⚠️  Errors: {result['errors']}")

