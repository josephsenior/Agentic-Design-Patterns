"""
Task Prioritization System - Prioritization Pattern

This module implements task prioritization for managing and ordering tasks
based on importance, urgency, and other criteria.
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class PriorityManager:
    """
    A system for prioritizing tasks based on multiple criteria.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.3,
        api_key: Optional[str] = None
    ):
        """Initialize the Priority Manager."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self.tasks = []
        self._build_prioritizer()
    
    def _build_prioritizer(self):
        """Build the prioritization chain."""
        
        self.priority_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a task prioritization expert. Evaluate tasks based on:

1. **Urgency**: How time-sensitive is this task?
2. **Importance**: How critical is this task to overall goals?
3. **Dependencies**: Does this task block other tasks?
4. **Effort**: How much work is required?
5. **Impact**: What's the potential impact of completing this task?

Assign a priority score from 1-10 (10 = highest priority) and provide reasoning."""),
            ("user", """Task: {task}
Context: {context}
Evaluate and assign priority score with reasoning.""")
        ])
        
        self.priority_chain = self.priority_prompt | self.llm | StrOutputParser()
    
    def add_task(
        self,
        task: str,
        context: str = "",
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Add a task and get its priority.
        
        Args:
            task: Task description
            context: Additional context
            metadata: Optional metadata
            
        Returns:
            Task with priority information
        """
        if not task or not task.strip():
            raise ValueError("Task cannot be empty")
        
        # Get priority
        priority_result = self.priority_chain.invoke({
            "task": task,
            "context": context or "No additional context"
        })
        
        # Extract priority score (simplified)
        priority_score = self._extract_priority_score(priority_result)
        
        task_data = {
            "id": len(self.tasks) + 1,
            "task": task,
            "context": context,
            "priority_score": priority_score,
            "priority_reasoning": priority_result,
            "metadata": metadata or {},
            "status": "pending"
        }
        
        self.tasks.append(task_data)
        return task_data
    
    def _extract_priority_score(self, text: str) -> float:
        """Extract priority score from text."""
        import re
        # Look for score patterns
        patterns = [
            r"priority.*?(\d+(?:\.\d+)?)",
            r"score.*?(\d+(?:\.\d+)?)",
            r"(\d+(?:\.\d+)?).*?priority"
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                score = float(match.group(1))
                return min(10, max(1, score))  # Clamp between 1-10
        return 5.0  # Default score
    
    def get_prioritized_tasks(self) -> List[Dict[str, Any]]:
        """Get tasks sorted by priority."""
        return sorted(
            self.tasks,
            key=lambda x: x["priority_score"],
            reverse=True
        )
    
    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Get the highest priority pending task."""
        pending = [t for t in self.tasks if t["status"] == "pending"]
        if not pending:
            return None
        return max(pending, key=lambda x: x["priority_score"])
    
    def complete_task(self, task_id: int):
        """Mark a task as completed."""
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if task:
            task["status"] = "completed"


if __name__ == "__main__":
    manager = PriorityManager()
    
    print("=" * 70)
    print("TASK PRIORITIZATION SYSTEM - PRIORITIZATION PATTERN")
    print("=" * 70)
    
    tasks = [
        ("Fix critical security bug", "Security vulnerability found in production"),
        ("Update documentation", "Documentation is outdated"),
        ("Implement new feature", "Customer requested feature"),
        ("Code review", "PR waiting for review"),
        ("Team meeting", "Scheduled for tomorrow")
    ]
    
    for task, context in tasks:
        print(f"\nAdding task: {task}")
        result = manager.add_task(task, context)
        print(f"   Priority Score: {result['priority_score']}/10")
    
    print("\n" + "=" * 70)
    print("PRIORITIZED TASK LIST")
    print("=" * 70)
    
    prioritized = manager.get_prioritized_tasks()
    for i, task in enumerate(prioritized, 1):
        print(f"\n{i}. {task['task']} (Priority: {task['priority_score']}/10)")
        print(f"   Context: {task['context']}")
    
    next_task = manager.get_next_task()
    if next_task:
        print(f"\nNext Task: {next_task['task']}")

