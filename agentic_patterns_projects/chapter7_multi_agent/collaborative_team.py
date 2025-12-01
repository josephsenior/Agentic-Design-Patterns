"""
Collaborative Team System - Multi-Agent Collaboration Pattern

This module demonstrates multiple specialized agents working together
to accomplish complex tasks through collaboration.
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class ResearchAgent:
    """Agent specialized in research and information gathering."""
    
    def __init__(self, llm):
        self.llm = llm
        self.role = "Researcher"
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research specialist. Your role is to gather 
comprehensive information on topics. Provide detailed, well-sourced information."""),
            ("user", "Research topic: {topic}")
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def research(self, topic: str) -> str:
        """Conduct research on a topic."""
        print(f"🔍 [{self.role}] Researching: {topic}")
        result = self.chain.invoke({"topic": topic})
        print(f"✅ [{self.role}] Research complete")
        return result


class WriterAgent:
    """Agent specialized in writing and content creation."""
    
    def __init__(self, llm):
        self.llm = llm
        self.role = "Writer"
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional writer. Your role is to create 
engaging, well-structured content based on research and requirements."""),
            ("user", """Write content based on the following:
Requirements: {requirements}
Research: {research}
Create engaging, well-structured content.""")
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def write(self, requirements: str, research: str) -> str:
        """Write content based on requirements and research."""
        print(f"✍️  [{self.role}] Writing content...")
        result = self.chain.invoke({
            "requirements": requirements,
            "research": research
        })
        print(f"✅ [{self.role}] Writing complete")
        return result


class EditorAgent:
    """Agent specialized in editing and quality control."""
    
    def __init__(self, llm):
        self.llm = llm
        self.role = "Editor"
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional editor. Your role is to review, 
improve, and polish content for clarity, style, and quality."""),
            ("user", """Edit and improve the following content:
Content: {content}
Provide an improved version with better clarity, flow, and quality.""")
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def edit(self, content: str) -> str:
        """Edit and improve content."""
        print(f"📝 [{self.role}] Editing content...")
        result = self.chain.invoke({"content": content})
        print(f"✅ [{self.role}] Editing complete")
        return result


class CoordinatorAgent:
    """Agent that coordinates the team's work."""
    
    def __init__(self, llm):
        self.llm = llm
        self.role = "Coordinator"
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a project coordinator. Your role is to synthesize 
work from multiple team members and create a final deliverable."""),
            ("user", """Synthesize the following team outputs:
Research: {research}
Draft: {draft}
Edited Version: {edited}
Create a final comprehensive deliverable.""")
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def coordinate(self, research: str, draft: str, edited: str) -> str:
        """Coordinate and synthesize team outputs."""
        print(f"👔 [{self.role}] Coordinating team outputs...")
        result = self.chain.invoke({
            "research": research,
            "draft": draft,
            "edited": edited
        })
        print(f"✅ [{self.role}] Coordination complete")
        return result


class CollaborativeTeam:
    """
    A team of specialized agents working together.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        """Initialize the Collaborative Team."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        # Initialize team members
        self.researcher = ResearchAgent(self.llm)
        self.writer = WriterAgent(self.llm)
        self.editor = EditorAgent(self.llm)
        self.coordinator = CoordinatorAgent(self.llm)
    
    def collaborate(
        self,
        task: str,
        requirements: str,
        research_topic: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a collaborative task with the team.
        
        Args:
            task: The overall task description
            requirements: Requirements for the deliverable
            research_topic: Optional specific research topic
            
        Returns:
            Dictionary with all team outputs
        """
        if not task or not requirements:
            raise ValueError("Task and requirements are required")
        
        research_topic = research_topic or task
        
        print("=" * 70)
        print("COLLABORATIVE TEAM - MULTI-AGENT COLLABORATION")
        print("=" * 70)
        print(f"\n📋 Task: {task}")
        print(f"📝 Requirements: {requirements}")
        
        # Step 1: Research
        print("\n" + "-" * 70)
        print("PHASE 1: RESEARCH")
        print("-" * 70)
        research = self.researcher.research(research_topic)
        
        # Step 2: Writing
        print("\n" + "-" * 70)
        print("PHASE 2: WRITING")
        print("-" * 70)
        draft = self.writer.write(requirements, research)
        
        # Step 3: Editing
        print("\n" + "-" * 70)
        print("PHASE 3: EDITING")
        print("-" * 70)
        edited = self.editor.edit(draft)
        
        # Step 4: Coordination
        print("\n" + "-" * 70)
        print("PHASE 4: COORDINATION")
        print("-" * 70)
        final = self.coordinator.coordinate(research, draft, edited)
        
        return {
            "task": task,
            "requirements": requirements,
            "research": research,
            "draft": draft,
            "edited": edited,
            "final": final,
            "team_members": [
                self.researcher.role,
                self.writer.role,
                self.editor.role,
                self.coordinator.role
            ]
        }
    
    def parallel_collaborate(
        self,
        tasks: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        Execute multiple collaborative tasks (can be parallelized).
        
        Args:
            tasks: List of task dictionaries with 'task' and 'requirements' keys
            
        Returns:
            List of collaboration results
        """
        results = []
        for task_dict in tasks:
            result = self.collaborate(
                task_dict["task"],
                task_dict["requirements"],
                task_dict.get("research_topic")
            )
            results.append(result)
        return results


if __name__ == "__main__":
    team = CollaborativeTeam()
    
    result = team.collaborate(
        task="Create a blog post about artificial intelligence",
        requirements="Write a 500-word blog post that explains AI in simple terms, includes examples, and is engaging for general audience.",
        research_topic="artificial intelligence basics and applications"
    )
    
    print("\n" + "=" * 70)
    print("FINAL DELIVERABLE")
    print("=" * 70)
    print(result["final"])

