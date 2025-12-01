"""
Reasoning Agent with Chain-of-Thought - Reasoning Techniques Pattern

This module implements Chain-of-Thought (CoT) reasoning for improved problem-solving.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class ReasoningAgent:
    """
    An agent that uses Chain-of-Thought reasoning for complex problem-solving.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.3,
        api_key: Optional[str] = None
    ):
        """Initialize the Reasoning Agent."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self._build_reasoning_chain()
    
    def _build_reasoning_chain(self):
        """Build the Chain-of-Thought reasoning chain."""
        
        self.cot_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a reasoning agent. When solving problems, think step-by-step:

1. **Analyze the Problem**: Break down the problem into components
2. **Identify Key Information**: Extract relevant facts and constraints
3. **Reason Step-by-Step**: Work through the solution logically
4. **Verify**: Check your reasoning for errors
5. **Conclude**: Provide the final answer

Show your reasoning process clearly before giving the final answer."""),
            ("user", """Problem: {problem}

Think through this step by step, showing your reasoning, then provide the answer.""")
        ])
        
        self.reasoning_chain = self.cot_prompt | self.llm | StrOutputParser()
    
    def solve(
        self,
        problem: str,
        show_reasoning: bool = True
    ) -> Dict[str, Any]:
        """
        Solve a problem using Chain-of-Thought reasoning.
        
        Args:
            problem: The problem to solve
            show_reasoning: Whether to include reasoning steps
            
        Returns:
            Dictionary with solution and reasoning
        """
        if not problem or not problem.strip():
            raise ValueError("Problem cannot be empty")
        
        response = self.reasoning_chain.invoke({"problem": problem})
        
        # Try to separate reasoning from answer
        if "answer:" in response.lower() or "conclusion:" in response.lower():
            parts = response.split("answer:", 1) if "answer:" in response.lower() else response.split("conclusion:", 1)
            reasoning = parts[0].strip()
            answer = parts[1].strip() if len(parts) > 1 else response
        else:
            reasoning = response
            answer = response
        
        return {
            "problem": problem,
            "full_response": response,
            "reasoning": reasoning if show_reasoning else None,
            "answer": answer
        }


class SelfCorrectingAgent:
    """
    An agent that can self-correct its reasoning.
    """
    
    def __init__(self, llm):
        self.llm = llm
    
    def solve_with_correction(self, problem: str) -> Dict[str, Any]:
        """
        Solve a problem with self-correction.
        
        Args:
            problem: The problem to solve
            
        Returns:
            Dictionary with solution and correction steps
        """
        # Initial attempt
        initial_prompt = ChatPromptTemplate.from_messages([
            ("system", "Solve this problem step by step."),
            ("user", f"Problem: {problem}")
        ])
        initial_chain = initial_prompt | self.llm | StrOutputParser()
        initial_solution = initial_chain.invoke({"problem": problem})
        
        # Self-correction
        correction_prompt = ChatPromptTemplate.from_messages([
            ("system", """Review the solution below. Check for errors, 
inconsistencies, or improvements. Provide a corrected version if needed."""),
            ("user", f"""Original Problem: {problem}
Initial Solution: {initial_solution}
Review and correct if necessary.""")
        ])
        correction_chain = correction_prompt | self.llm | StrOutputParser()
        corrected_solution = correction_chain.invoke({
            "problem": problem,
            "initial_solution": initial_solution
        })
        
        return {
            "problem": problem,
            "initial_solution": initial_solution,
            "corrected_solution": corrected_solution,
            "was_corrected": initial_solution != corrected_solution
        }


if __name__ == "__main__":
    agent = ReasoningAgent()
    
    print("=" * 70)
    print("REASONING AGENT - CHAIN-OF-THOUGHT PATTERN")
    print("=" * 70)
    
    problems = [
        "If a train travels 60 miles per hour and needs to cover 180 miles, how long will it take?",
        "Explain the main differences between classical and quantum computers.",
        "A store has 20% off sale. An item originally costs $100. What's the final price?"
    ]
    
    for problem in problems:
        print(f"\n{'='*70}")
        print(f"📋 Problem: {problem}")
        print("=" * 70)
        result = agent.solve(problem)
        print(f"\n💭 Reasoning:\n{result['reasoning']}")
        print(f"\n✅ Answer: {result['answer']}")

