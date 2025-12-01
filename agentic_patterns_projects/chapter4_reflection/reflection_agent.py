"""
Self-Improving Content Generator - Reflection Pattern Implementation

This module implements a reflection pattern where an agent generates content,
critiques it, and then refines it based on the critique.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()


class ReflectionAgent:
    """
    An agent that uses reflection to improve its output through self-critique.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        """Initialize the Reflection Agent."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self._build_reflection_chain()
    
    def _build_reflection_chain(self):
        """Build the reflection chain: Generate → Critique → Refine."""
        
        # Step 1: Initial Generation
        self.generation_chain = (
            ChatPromptTemplate.from_messages([
                ("system", "You are a creative content writer. Write clear, engaging content based on the given requirements."),
                ("user", "{requirements}")
            ])
            | self.llm
            | StrOutputParser()
        )
        
        # Step 2: Critique
        self.critique_chain = (
            ChatPromptTemplate.from_messages([
                ("system", """You are a quality reviewer. Critically evaluate the following content 
based on:
- Clarity and readability
- Structure and organization
- Engagement and appeal
- Completeness
- Grammar and style

Provide specific, actionable feedback for improvement."""),
                ("user", "Content to Critique:\n{initial_content}\n\nOriginal Requirements: {requirements}")
            ])
            | self.llm
            | StrOutputParser()
        )
        
        # Step 3: Refinement
        self.refinement_chain = (
            ChatPromptTemplate.from_messages([
                ("system", """You are an expert content editor. Based on the original requirements 
and the critique provided, rewrite the content to address all feedback while maintaining 
the core message and improving quality.

Original Requirements: {requirements}
Critique: {critique}

Create an improved version that addresses all the critique points."""),
                ("user", "Original Content:\n{initial_content}")
            ])
            | self.llm
            | StrOutputParser()
        )
        
        # Build the full reflection chain
        self.full_reflection_chain = (
            RunnablePassthrough.assign(
                initial_content=self.generation_chain
            )
            | RunnablePassthrough.assign(
                critique=self.critique_chain
            )
            | self.refinement_chain
        )
    
    def generate_with_reflection(
        self,
        requirements: str,
        return_intermediate: bool = False
    ) -> Dict[str, Any]:
        """
        Generate content using the reflection pattern.
        
        Args:
            requirements: The requirements for the content to generate
            return_intermediate: If True, return intermediate steps
            
        Returns:
            Dictionary with final content and optionally intermediate steps
        """
        if not requirements or not requirements.strip():
            raise ValueError("Requirements cannot be empty")
        
        if return_intermediate:
            # Execute step by step to capture intermediate results
            initial = self.generation_chain.invoke({"requirements": requirements})
            critique = self.critique_chain.invoke({
                "initial_content": initial,
                "requirements": requirements
            })
            refined = self.refinement_chain.invoke({
                "initial_content": initial,
                "critique": critique,
                "requirements": requirements
            })
            
            return {
                "initial_content": initial,
                "critique": critique,
                "refined_content": refined,
                "requirements": requirements
            }
        else:
            # Execute full chain
            refined = self.full_reflection_chain.invoke({"requirements": requirements})
            return {
                "refined_content": refined,
                "requirements": requirements
            }
    
    def iterative_reflection(
        self,
        requirements: str,
        iterations: int = 2
    ) -> Dict[str, Any]:
        """
        Apply reflection multiple times for iterative improvement.
        
        Args:
            requirements: The requirements for the content
            iterations: Number of reflection cycles
            
        Returns:
            Dictionary with all iteration results
        """
        if iterations < 1:
            raise ValueError("Iterations must be at least 1")
        
        results = {
            "requirements": requirements,
            "iterations": []
        }
        
        current_content = None
        
        for i in range(iterations):
            if i == 0:
                # First iteration: generate initial content
                current_content = self.generation_chain.invoke({"requirements": requirements})
            else:
                # Subsequent iterations: use previous refined content as starting point
                current_content = results["iterations"][-1]["refined_content"]
            
            # Critique
            critique = self.critique_chain.invoke({
                "initial_content": current_content,
                "requirements": requirements
            })
            
            # Refine
            refined = self.refinement_chain.invoke({
                "initial_content": current_content,
                "critique": critique,
                "requirements": requirements
            })
            
            results["iterations"].append({
                "iteration": i + 1,
                "initial_content": current_content,
                "critique": critique,
                "refined_content": refined
            })
        
        return results


if __name__ == "__main__":
    agent = ReflectionAgent()
    
    requirements = "Write a product description for a smart coffee mug that keeps coffee hot and can be controlled via smartphone app."
    
    print("=" * 70)
    print("REFLECTION AGENT - SELF-IMPROVING CONTENT GENERATOR")
    print("=" * 70)
    
    print("\nRequirements:", requirements)
    print("\n" + "=" * 70)
    print("GENERATING WITH REFLECTION...")
    print("=" * 70)
    
    result = agent.generate_with_reflection(requirements, return_intermediate=True)
    
    print("\n" + "-" * 70)
    print("STEP 1: INITIAL GENERATION")
    print("-" * 70)
    print(result["initial_content"])
    
    print("\n" + "-" * 70)
    print("STEP 2: CRITIQUE")
    print("-" * 70)
    print(result["critique"])
    
    print("\n" + "-" * 70)
    print("STEP 3: REFINED CONTENT")
    print("-" * 70)
    print(result["refined_content"])

