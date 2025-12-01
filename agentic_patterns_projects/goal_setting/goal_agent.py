"""
Goal-Oriented Agent - Goal Setting and Monitoring Pattern

This module implements goal setting and monitoring for agents that work
towards specific objectives with progress tracking.
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class GoalAgent:
    """
    An agent that sets goals and monitors progress towards achieving them.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.3,
        api_key: Optional[str] = None
    ):
        """Initialize the Goal Agent."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self.goals = []
        self.progress_history = []
        self._build_chains()
    
    def _build_chains(self):
        """Build goal setting and monitoring chains."""
        
        # Goal breakdown chain
        self.goal_breakdown_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a goal planning specialist. Break down goals into 
specific, measurable, achievable, relevant, and time-bound (SMART) sub-goals.

For each sub-goal, provide:
- Description
- Success criteria
- Estimated steps to complete"""),
            ("user", "Goal: {goal}\n\nBreak this down into actionable sub-goals.")
        ])
        
        self.breakdown_chain = self.goal_breakdown_prompt | self.llm | StrOutputParser()
        
        # Progress assessment chain
        self.progress_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a progress monitor. Assess progress towards goals 
and provide:
- Current status
- Completed steps
- Remaining work
- Recommendations for next steps"""),
            ("user", """Goal: {goal}
Sub-goals: {sub_goals}
Completed actions: {completed_actions}
Assess progress and provide recommendations.""")
        ])
        
        self.progress_chain = self.progress_prompt | self.llm | StrOutputParser()
    
    def set_goal(self, goal: str) -> Dict[str, Any]:
        """
        Set a new goal and break it down into sub-goals.
        
        Args:
            goal: The main goal to achieve
            
        Returns:
            Dictionary with goal and sub-goals
        """
        if not goal or not goal.strip():
            raise ValueError("Goal cannot be empty")
        
        # Break down goal
        sub_goals_text = self.breakdown_chain.invoke({"goal": goal})
        
        goal_data = {
            "id": len(self.goals) + 1,
            "goal": goal,
            "sub_goals": sub_goals_text,
            "status": "active",
            "progress": 0,
            "completed_actions": [],
            "created_at": "now"
        }
        
        self.goals.append(goal_data)
        
        return goal_data
    
    def update_progress(
        self,
        goal_id: int,
        completed_action: str
    ) -> Dict[str, Any]:
        """
        Update progress on a goal.
        
        Args:
            goal_id: The ID of the goal
            completed_action: Description of completed action
            
        Returns:
            Updated goal data with progress assessment
        """
        goal = next((g for g in self.goals if g["id"] == goal_id), None)
        if not goal:
            raise ValueError(f"Goal {goal_id} not found")
        
        # Add completed action
        goal["completed_actions"].append(completed_action)
        
        # Assess progress
        progress_assessment = self.progress_chain.invoke({
            "goal": goal["goal"],
            "sub_goals": goal["sub_goals"],
            "completed_actions": "\n".join(goal["completed_actions"])
        })
        
        # Update progress percentage (simplified)
        total_actions = len(goal["completed_actions"])
        goal["progress"] = min(100, (total_actions * 10))  # Simplified calculation
        
        # Check if goal is complete
        if "complete" in progress_assessment.lower() or goal["progress"] >= 100:
            goal["status"] = "completed"
        
        self.progress_history.append({
            "goal_id": goal_id,
            "action": completed_action,
            "assessment": progress_assessment,
            "timestamp": "now"
        })
        
        return {
            "goal": goal,
            "progress_assessment": progress_assessment
        }
    
    def get_goal_status(self, goal_id: int) -> Dict[str, Any]:
        """Get the current status of a goal."""
        goal = next((g for g in self.goals if g["id"] == goal_id), None)
        if not goal:
            raise ValueError(f"Goal {goal_id} not found")
        
        return goal
    
    def list_goals(self) -> List[Dict[str, Any]]:
        """List all goals."""
        return self.goals


if __name__ == "__main__":
    agent = GoalAgent()
    
    print("=" * 70)
    print("GOAL-ORIENTED AGENT - GOAL SETTING AND MONITORING")
    print("=" * 70)
    
    # Set a goal
    goal = "Create a marketing campaign for a new product"
    print(f"\nSetting goal: {goal}")
    goal_data = agent.set_goal(goal)
    print(f"\nSub-goals:\n{goal_data['sub_goals']}")
    
    # Update progress
    print(f"\nUpdating progress...")
    progress = agent.update_progress(goal_data["id"], "Created campaign strategy document")
    print(f"Progress: {progress['goal']['progress']}%")
    print(f"Assessment: {progress['progress_assessment'][:200]}...")

