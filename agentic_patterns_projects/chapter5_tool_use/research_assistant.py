"""
Research Assistant with Tools - Tool Use Pattern Implementation

This module demonstrates how agents can use external tools to extend their capabilities,
such as searching for information, performing calculations, or accessing APIs.
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

load_dotenv()


# Define custom tools
@tool
def search_information(query: str) -> str:
    """
    Search for factual information on a given topic.
    Use this tool to find answers to questions about facts, data, or general knowledge.
    
    Args:
        query: The search query or question
        
    Returns:
        Information about the query
    """
    print(f"\n[TOOL] Searching for: '{query}'")
    
    # Simulated search results (in production, this would call a real search API)
    knowledge_base = {
        "capital of france": "The capital of France is Paris, located in the north-central part of the country.",
        "weather in london": "London typically has a temperate maritime climate with mild winters and cool summers. Current conditions vary by season.",
        "population of earth": "As of 2024, the estimated population of Earth is approximately 8.1 billion people.",
        "tallest mountain": "Mount Everest, located in the Himalayas on the border between Nepal and China, is the tallest mountain above sea level at 8,848.86 meters (29,031.7 feet).",
        "largest ocean": "The Pacific Ocean is the largest ocean, covering approximately 63 million square miles.",
        "python programming": "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used in web development, data science, AI, and automation.",
    }
    
    query_lower = query.lower().strip()
    result = knowledge_base.get(query_lower, 
        f"Information about '{query}': This is a simulated search result. In a real implementation, this would query a search engine or knowledge base.")
    
    print(f"[TOOL] Result: {result[:100]}...")
    return result


@tool
def calculate(expression: str) -> str:
    """
    Perform mathematical calculations.
    Use this tool to solve math problems, compute values, or perform calculations.
    
    Args:
        expression: A mathematical expression to evaluate (e.g., "2 + 2", "100 * 0.15")
        
    Returns:
        The calculated result
    """
    print(f"\n[TOOL] Calculating: '{expression}'")
    
    try:
        # Safe evaluation of mathematical expressions
        allowed_chars = set('0123456789+-*/()., ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression. Only basic math operations are allowed."
        
        result = eval(expression)
        print(f"[TOOL] Result: {result}")
        return str(result)
    except Exception as e:
        error_msg = f"Error calculating '{expression}': {str(e)}"
        print(f"[TOOL] Error: {error_msg}")
        return error_msg


@tool
def get_current_time() -> str:
    """
    Get the current date and time.
    Use this tool when the user asks about the current time, date, or day.
    
    Returns:
        Current date and time information
    """
    from datetime import datetime
    print(f"\n[TOOL] Getting current time...")
    now = datetime.now()
    result = f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')} ({now.strftime('%A')})"
    print(f"[TOOL] {result}")
    return result


@tool
def word_count(text: str) -> str:
    """
    Count words, characters, and sentences in a given text.
    Use this tool when the user wants to analyze text statistics.
    
    Args:
        text: The text to analyze
        
    Returns:
        Text statistics
    """
    print(f"\n[TOOL] Analyzing text...")
    words = len(text.split())
    chars = len(text)
    chars_no_spaces = len(text.replace(' ', ''))
    sentences = text.count('.') + text.count('!') + text.count('?')
    
    result = f"Text Statistics:\n- Words: {words}\n- Characters: {chars}\n- Characters (no spaces): {chars_no_spaces}\n- Sentences: {sentences}"
    print(f"[TOOL] {result}")
    return result


class ResearchAssistant:
    """
    A research assistant agent that can use tools to answer questions and perform tasks.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0,
        api_key: Optional[str] = None,
        tools: Optional[List] = None
    ):
        """
        Initialize the Research Assistant.
        
        Args:
            model_name: The OpenAI model to use
            temperature: Sampling temperature
            api_key: OpenAI API key
            tools: Custom tools to use (defaults to built-in tools)
        """
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        # Use provided tools or default tools
        self.tools = tools or [
            search_information,
            calculate,
            get_current_time,
            word_count
        ]
        
        self._build_agent()
    
    def _build_agent(self):
        """Build the tool-calling agent."""
        # Create the agent prompt
        agent_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful research assistant. You have access to various tools 
to help answer questions and perform tasks. When you need information, use the appropriate tool. 
Always explain your reasoning and cite the tools you use."""),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        # Create the agent
        self.agent = create_tool_calling_agent(self.llm, self.tools, agent_prompt)
        
        # Create the executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def ask(self, question: str) -> Dict[str, Any]:
        """
        Ask a question to the research assistant.
        
        Args:
            question: The question or request
            
        Returns:
            Dictionary with the response
        """
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        
        try:
            result = self.agent_executor.invoke({"input": question})
            return {
                "question": question,
                "answer": result["output"],
                "success": True
            }
        except Exception as e:
            return {
                "question": question,
                "answer": None,
                "error": str(e),
                "success": False
            }
    
    async def ask_async(self, question: str) -> Dict[str, Any]:
        """
        Ask a question asynchronously.
        
        Args:
            question: The question or request
            
        Returns:
            Dictionary with the response
        """
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        
        try:
            result = await self.agent_executor.ainvoke({"input": question})
            return {
                "question": question,
                "answer": result["output"],
                "success": True
            }
        except Exception as e:
            return {
                "question": question,
                "answer": None,
                "error": str(e),
                "success": False
            }


if __name__ == "__main__":
    assistant = ResearchAssistant()
    
    print("=" * 70)
    print("RESEARCH ASSISTANT - TOOL USE PATTERN")
    print("=" * 70)
    
    questions = [
        "What is the capital of France?",
        "Calculate 25 * 4 + 100",
        "What's the current time?",
        "Count the words in this text: 'The quick brown fox jumps over the lazy dog.'",
        "What is the tallest mountain in the world?",
    ]
    
    for question in questions:
        print(f"\n{'='*70}")
        print(f"Question: {question}")
        print("=" * 70)
        result = assistant.ask(question)
        if result["success"]:
            print(f"\nAnswer: {result['answer']}")
        else:
            print(f"\n❌ Error: {result.get('error', 'Unknown error')}")

