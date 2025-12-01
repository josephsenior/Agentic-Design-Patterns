"""
Agent Evaluation System - Evaluation and Monitoring Pattern

This module implements evaluation and monitoring for agent performance
using LLM-as-a-Judge and other evaluation techniques.
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class AgentEvaluator:
    """
    An evaluation system that assesses agent responses using LLM-as-a-Judge.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0,
        api_key: Optional[str] = None
    ):
        """Initialize the Agent Evaluator."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self._build_evaluator()
    
    def _build_evaluator(self):
        """Build the evaluation chain."""
        
        self.evaluation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert evaluator. Evaluate agent responses based on:

1. **Correctness**: Is the information accurate and correct?
2. **Relevance**: Does it address the question/request?
3. **Completeness**: Is the response complete?
4. **Clarity**: Is it clear and well-structured?
5. **Helpfulness**: Is it useful and actionable?

Provide scores from 1-10 for each criterion and an overall assessment."""),
            ("user", """Question/Request: {query}
Agent Response: {response}

Evaluate this response and provide:
- Scores for each criterion (1-10)
- Overall score (1-10)
- Strengths
- Areas for improvement""")
        ])
        
        self.evaluation_chain = self.evaluation_prompt | self.llm | StrOutputParser()
    
    def evaluate(
        self,
        query: str,
        response: str
    ) -> Dict[str, Any]:
        """
        Evaluate an agent response.
        
        Args:
            query: The original query/request
            response: The agent's response
            
        Returns:
            Dictionary with evaluation results
        """
        if not query or not response:
            raise ValueError("Query and response are required")
        
        evaluation = self.evaluation_chain.invoke({
            "query": query,
            "response": response
        })
        
        # Try to extract scores (simplified parsing)
        scores = {
            "correctness": self._extract_score(evaluation, "correctness"),
            "relevance": self._extract_score(evaluation, "relevance"),
            "completeness": self._extract_score(evaluation, "completeness"),
            "clarity": self._extract_score(evaluation, "clarity"),
            "helpfulness": self._extract_score(evaluation, "helpfulness"),
            "overall": self._extract_score(evaluation, "overall")
        }
        
        return {
            "query": query,
            "response": response,
            "evaluation": evaluation,
            "scores": scores,
            "average_score": sum(scores.values()) / len(scores) if scores.values() else 0
        }
    
    def _extract_score(self, text: str, criterion: str) -> float:
        """Extract score for a criterion from evaluation text."""
        import re
        pattern = rf"{criterion}.*?(\d+(?:\.\d+)?)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))
        return 0.0
    
    def compare_responses(
        self,
        query: str,
        responses: List[str]
    ) -> Dict[str, Any]:
        """
        Compare multiple agent responses.
        
        Args:
            query: The original query
            responses: List of responses to compare
            
        Returns:
            Comparison results
        """
        evaluations = []
        for i, response in enumerate(responses):
            eval_result = self.evaluate(query, response)
            evaluations.append({
                "response_id": i + 1,
                "response": response,
                "evaluation": eval_result
            })
        
        # Find best response
        best = max(evaluations, key=lambda x: x["evaluation"]["average_score"])
        
        return {
            "query": query,
            "evaluations": evaluations,
            "best_response": best,
            "total_responses": len(responses)
        }


if __name__ == "__main__":
    evaluator = AgentEvaluator()
    
    print("=" * 70)
    print("AGENT EVALUATION SYSTEM - EVALUATION AND MONITORING")
    print("=" * 70)
    
    query = "What is artificial intelligence?"
    response = "Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines capable of performing tasks that typically require human intelligence."
    
    print(f"\nQuery: {query}")
    print(f"Response: {response}")
    
    result = evaluator.evaluate(query, response)
    print(f"\nEvaluation:\n{result['evaluation']}")
    print(f"\nAverage Score: {result['average_score']:.2f}/10")

