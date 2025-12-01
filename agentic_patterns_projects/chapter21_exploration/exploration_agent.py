"""
Agent Laboratory - Exploration and Discovery Pattern

This module implements exploration strategies for agents to discover
new solutions and approaches through experimentation.
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import random

load_dotenv()


class ExplorationAgent:
    """
    An agent that explores different approaches to solve problems.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.9,  # Higher temperature for exploration
        api_key: Optional[str] = None
    ):
        """Initialize the Exploration Agent."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self.experiments = []
        self._build_explorer()
    
    def _build_explorer(self):
        """Build the exploration chain."""
        
        self.exploration_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an experimental agent. Explore creative and 
unconventional approaches to problems. Think outside the box and propose 
multiple alternative solutions."""),
            ("user", """Problem: {problem}
Approach: {approach}
Explore this approach and provide a creative solution.""")
        ])
        
        self.chain = self.exploration_prompt | self.llm | StrOutputParser()
    
    def explore(
        self,
        problem: str,
        num_approaches: int = 3
    ) -> Dict[str, Any]:
        """
        Explore multiple approaches to a problem.
        
        Args:
            problem: The problem to solve
            num_approaches: Number of different approaches to try
            
        Returns:
            Dictionary with exploration results
        """
        approaches = [
            "analytical",
            "creative",
            "practical",
            "innovative",
            "systematic"
        ]
        
        selected_approaches = random.sample(approaches, min(num_approaches, len(approaches)))
        
        results = []
        for approach in selected_approaches:
            print(f"🔬 Exploring {approach} approach...")
            solution = self.chain.invoke({
                "problem": problem,
                "approach": approach
            })
            
            experiment = {
                "approach": approach,
                "solution": solution,
                "problem": problem
            }
            results.append(experiment)
            self.experiments.append(experiment)
        
        return {
            "problem": problem,
            "approaches_explored": len(results),
            "solutions": results
        }
    
    def compare_solutions(self, problem: str) -> Dict[str, Any]:
        """
        Generate and compare multiple solutions.
        
        Args:
            problem: The problem to solve
            
        Returns:
            Comparison of different solutions
        """
        exploration = self.explore(problem, num_approaches=3)
        
        # Simple comparison (in production, use evaluation)
        return {
            "problem": problem,
            "solutions": exploration["solutions"],
            "recommendation": "Review all approaches and select the most suitable one."
        }


if __name__ == "__main__":
    agent = ExplorationAgent()
    
    print("=" * 70)
    print("EXPLORATION AGENT - EXPLORATION AND DISCOVERY PATTERN")
    print("=" * 70)
    
    problem = "How can we improve user engagement in a mobile app?"
    
    print(f"\n🔍 Problem: {problem}")
    print("\n" + "=" * 70)
    print("EXPLORING MULTIPLE APPROACHES")
    print("=" * 70)
    
    result = agent.explore(problem, num_approaches=3)
    
    for i, solution in enumerate(result["solutions"], 1):
        print(f"\n{'='*70}")
        print(f"Approach {i}: {solution['approach'].upper()}")
        print("=" * 70)
        print(solution['solution'][:300] + "...")

