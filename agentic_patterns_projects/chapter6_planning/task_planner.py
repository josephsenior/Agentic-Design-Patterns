"""
Task Planning System - Planning Pattern Implementation

This module implements a planning pattern where an agent breaks down complex goals
into actionable, sequential tasks.
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import re

load_dotenv()


class TaskPlanner:
    """
    A planning agent that decomposes goals into actionable tasks.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.3,
        api_key: Optional[str] = None
    ):
        """Initialize the Task Planner."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self._build_planner()
    
    def _build_planner(self):
        """Build the planning chain."""
        
        # Step 1: Create a plan
        self.planning_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert project planner. Break down the given goal into 
a detailed, actionable plan with sequential steps.

For each step, provide:
- Step number
- Task description
- Expected outcome
- Dependencies (if any)

Format your response as a structured plan that can be executed step by step."""),
            ("user", "Goal: {goal}\n\nCreate a detailed plan to achieve this goal.")
        ])
        
        self.planning_chain = (
            self.planning_prompt
            | self.llm
            | StrOutputParser()
        )
        
        # Step 2: Execute tasks (simulated)
        self.execution_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a task executor. Given a task from the plan, 
execute it and provide the result. Be specific and actionable."""),
            ("user", """Plan Context: {plan_context}
Current Task: {task}
Previous Results: {previous_results}

Execute this task and provide the result.""")
        ])
        
        self.execution_chain = (
            self.execution_prompt
            | self.llm
            | StrOutputParser()
        )
    
    def create_plan(self, goal: str) -> Dict[str, Any]:
        """
        Create a plan for achieving a goal.
        
        Args:
            goal: The goal to plan for
            
        Returns:
            Dictionary with the plan
        """
        if not goal or not goal.strip():
            raise ValueError("Goal cannot be empty")
        
        plan_text = self.planning_chain.invoke({"goal": goal})
        
        # Parse plan into structured format
        tasks = self._parse_plan(plan_text)
        
        return {
            "goal": goal,
            "plan_text": plan_text,
            "tasks": tasks,
            "total_tasks": len(tasks)
        }
    
    def _parse_plan(self, plan_text: str) -> List[Dict[str, Any]]:
        """Parse plan text into structured tasks."""
        tasks = []
        lines = plan_text.split('\n')
        
        current_task = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for step numbers
            step_match = re.match(r'^(\d+)\.?\s*(.+)', line)
            if step_match:
                if current_task:
                    tasks.append(current_task)
                
                current_task = {
                    "step": int(step_match.group(1)),
                    "description": step_match.group(2),
                    "outcome": "",
                    "dependencies": []
                }
            elif current_task:
                # Look for outcome or dependency indicators
                if line.lower().startswith(('outcome:', 'result:', 'expected:')):
                    current_task["outcome"] = line.split(':', 1)[1].strip()
                elif line.lower().startswith(('depends on:', 'dependency:', 'requires:')):
                    deps = line.split(':', 1)[1].strip()
                    current_task["dependencies"] = [d.strip() for d in deps.split(',')]
                else:
                    # Append to description if it's continuation
                    if not current_task["outcome"]:
                        current_task["description"] += " " + line
        
        if current_task:
            tasks.append(current_task)
        
        return tasks
    
    def execute_plan(self, plan: Dict[str, Any], execute_tasks: bool = True) -> Dict[str, Any]:
        """
        Execute a plan step by step.
        
        Args:
            plan: The plan dictionary from create_plan
            execute_tasks: Whether to actually execute tasks or just return the plan
            
        Returns:
            Dictionary with execution results
        """
        if not execute_tasks:
            return {
                "plan": plan,
                "executed": False,
                "message": "Plan created but not executed"
            }
        
        results = {
            "plan": plan,
            "execution_results": [],
            "completed": False
        }
        
        previous_results = []
        
        for task in plan["tasks"]:
            print(f"\n📋 Executing Step {task['step']}: {task['description']}")
            
            # Build context
            plan_context = f"Goal: {plan['goal']}\n\nPlan:\n{plan['plan_text']}"
            previous_context = "\n".join([
                f"Step {r['step']}: {r['result'][:100]}..."
                for r in previous_results
            ]) if previous_results else "No previous steps completed."
            
            # Execute task
            result = self.execution_chain.invoke({
                "plan_context": plan_context,
                "task": task["description"],
                "previous_results": previous_context
            })
            
            execution_result = {
                "step": task["step"],
                "task": task["description"],
                "result": result,
                "completed": True
            }
            
            results["execution_results"].append(execution_result)
            previous_results.append(execution_result)
            
            print(f"✅ Step {task['step']} completed")
        
        results["completed"] = True
        return results
    
    def plan_and_execute(self, goal: str, execute: bool = True) -> Dict[str, Any]:
        """
        Create a plan and optionally execute it.
        
        Args:
            goal: The goal to achieve
            execute: Whether to execute the plan
            
        Returns:
            Complete planning and execution results
        """
        print(f"🎯 Goal: {goal}")
        print("\n" + "=" * 70)
        print("PLANNING PHASE")
        print("=" * 70)
        
        plan = self.create_plan(goal)
        
        print(f"\n📝 Plan created with {plan['total_tasks']} tasks:")
        for task in plan["tasks"]:
            print(f"  {task['step']}. {task['description']}")
        
        if execute:
            print("\n" + "=" * 70)
            print("EXECUTION PHASE")
            print("=" * 70)
            execution_results = self.execute_plan(plan, execute_tasks=True)
            return {
                "plan": plan,
                "execution": execution_results
            }
        else:
            return {
                "plan": plan,
                "execution": None
            }


if __name__ == "__main__":
    planner = TaskPlanner()
    
    goal = "Create a marketing campaign for a new product launch"
    
    print("=" * 70)
    print("TASK PLANNER - PLANNING PATTERN")
    print("=" * 70)
    
    result = planner.plan_and_execute(goal, execute=True)
    
    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    
    if result["execution"]:
        for exec_result in result["execution"]["execution_results"]:
            print(f"\nStep {exec_result['step']}: {exec_result['task']}")
            print(f"Result: {exec_result['result'][:200]}...")

