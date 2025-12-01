"""
Adaptive Agent - Adaptation Pattern

This module implements an adaptive system that improves its performance
over time based on feedback and experience.
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class AdaptiveAgent:
    """
    An agent that adapts and improves based on feedback.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        """Initialize the Adaptive Agent."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self.interaction_history = []
        self.performance_metrics = {
            "total_interactions": 0,
            "successful_interactions": 0,
            "average_rating": 0.0
        }
        self.learned_patterns = []
        self._build_agent()
    
    def _build_agent(self):
        """Build the adaptive agent chain."""
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an adaptive assistant. Learn from past interactions 
to improve your responses. Consider what worked well in previous conversations.

Learned patterns:
{learned_patterns}

Previous successful interactions:
{successful_examples}

Use this knowledge to provide better responses."""),
            ("user", "{query}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def process(
        self,
        query: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a query with adaptive learning.
        
        Args:
            query: User query
            context: Optional context
            
        Returns:
            Response with adaptation info
        """
        # Build learned patterns string
        patterns_str = "\n".join(self.learned_patterns[-5:]) if self.learned_patterns else "No patterns learned yet"
        
        # Get successful examples
        successful = [h for h in self.interaction_history if h.get("rating", 0) >= 4]
        examples_str = "\n".join([
            f"Q: {h['query']}\nA: {h['response'][:100]}..."
            for h in successful[-3:]
        ]) if successful else "No examples yet"
        
        # Generate response
        response = self.chain.invoke({
            "query": query,
            "learned_patterns": patterns_str,
            "successful_examples": examples_str
        })
        
        # Record interaction
        interaction = {
            "query": query,
            "response": response,
            "context": context,
            "timestamp": "now"
        }
        self.interaction_history.append(interaction)
        self.performance_metrics["total_interactions"] += 1
        
        return {
            "query": query,
            "response": response,
            "interaction_id": len(self.interaction_history)
        }
    
    def provide_feedback(
        self,
        interaction_id: int,
        rating: float,
        feedback_text: Optional[str] = None
    ):
        """
        Provide feedback on an interaction to enable learning.
        
        Args:
            interaction_id: ID of the interaction
            rating: Rating from 1-5
            feedback_text: Optional feedback text
        """
        if interaction_id < 1 or interaction_id > len(self.interaction_history):
            raise ValueError("Invalid interaction ID")
        
        interaction = self.interaction_history[interaction_id - 1]
        interaction["rating"] = rating
        interaction["feedback"] = feedback_text
        
        if rating >= 4:
            self.performance_metrics["successful_interactions"] += 1
        
        # Update average rating
        ratings = [h.get("rating", 0) for h in self.interaction_history if "rating" in h]
        if ratings:
            self.performance_metrics["average_rating"] = sum(ratings) / len(ratings)
        
        # Learn from feedback
        if feedback_text and rating >= 4:
            pattern = f"Successful pattern: {feedback_text}"
            self.learned_patterns.append(pattern)
            print(f"📚 Learned new pattern: {pattern[:50]}...")
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        return {
            **self.performance_metrics,
            "learned_patterns_count": len(self.learned_patterns),
            "total_feedback": len([h for h in self.interaction_history if "rating" in h])
        }


if __name__ == "__main__":
    agent = AdaptiveAgent()
    
    print("=" * 70)
    print("ADAPTIVE AGENT - ADAPTATION PATTERN")
    print("=" * 70)
    
    # Simulate interactions with feedback
    queries = [
        "What is machine learning?",
        "Explain neural networks",
        "How does deep learning work?"
    ]
    
    for query in queries:
        print(f"\n❓ Query: {query}")
        result = agent.process(query)
        print(f"💬 Response: {result['response'][:100]}...")
        
        # Simulate feedback
        rating = 4.5
        agent.provide_feedback(result['interaction_id'], rating, "Clear and helpful explanation")
    
    print("\n" + "=" * 70)
    print("PERFORMANCE STATISTICS")
    print("=" * 70)
    stats = agent.get_performance_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")

