"""
Interactive Agent with Human-in-the-Loop - Human-in-the-Loop Pattern

This module implements human-in-the-loop interactions for customer support
and scenarios requiring human oversight.
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class InteractiveAgent:
    """
    An agent that can escalate to human support when needed.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        """Initialize the Interactive Agent."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self.conversation_history = []
        self.escalation_count = 0
        self._build_agent()
    
    def _build_agent(self):
        """Build the interactive agent chain."""
        
        # Decision prompt - decides if escalation is needed
        self.decision_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a customer support agent. Analyze the user's request 
and determine if you can handle it or if it needs human escalation.

Respond with:
- "handle" if you can resolve the issue
- "escalate" if human intervention is needed

Consider escalating for:
- Complex technical issues
- Billing disputes
- Account security concerns
- Requests for refunds
- Issues requiring account access changes"""),
            ("user", """User message: {message}
Conversation history: {history}""")
        ])
        
        self.decision_chain = self.decision_prompt | self.llm | StrOutputParser()
        
        # Response prompt
        self.response_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful customer support agent. Provide clear, 
empathetic responses. Reference conversation history when relevant."""),
            ("user", """User message: {message}
Conversation history: {history}
Provide a helpful response.""")
        ])
        
        self.response_chain = self.response_prompt | self.llm | StrOutputParser()
    
    def process_message(
        self,
        message: str,
        auto_escalate: bool = False
    ) -> Dict[str, Any]:
        """
        Process a user message with potential human escalation.
        
        Args:
            message: User's message
            auto_escalate: If True, automatically escalate after 3 interactions
            
        Returns:
            Dictionary with response and escalation status
        """
        # Build conversation history string
        history_str = "\n".join([
            f"User: {h['user']}\nAgent: {h['agent']}"
            for h in self.conversation_history[-5:]
        ]) if self.conversation_history else "No previous conversation"
        
        # Check if auto-escalation is needed
        if auto_escalate and len(self.conversation_history) >= 3:
            return {
                "response": "I'm transferring you to a human specialist who can better assist you.",
                "escalated": True,
                "reason": "Auto-escalation after multiple interactions"
            }
        
        # Decide if escalation is needed
        decision = self.decision_chain.invoke({
            "message": message,
            "history": history_str
        }).strip().lower()
        
        if "escalate" in decision:
            self.escalation_count += 1
            return {
                "response": "I'm connecting you with a human specialist who can better assist with this issue. Please hold...",
                "escalated": True,
                "reason": "Complex issue requiring human expertise"
            }
        
        # Generate response
        response = self.response_chain.invoke({
            "message": message,
            "history": history_str
        })
        
        # Update conversation history
        self.conversation_history.append({
            "user": message,
            "agent": response
        })
        
        return {
            "response": response,
            "escalated": False,
            "conversation_length": len(self.conversation_history)
        }
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the conversation."""
        return {
            "total_exchanges": len(self.conversation_history),
            "escalations": self.escalation_count,
            "history": self.conversation_history
        }
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
        self.escalation_count = 0
        print("🔄 Conversation reset")


if __name__ == "__main__":
    agent = InteractiveAgent()
    
    print("=" * 70)
    print("INTERACTIVE AGENT - HUMAN-IN-THE-LOOP PATTERN")
    print("=" * 70)
    
    messages = [
        "I can't log into my account",
        "I've tried resetting my password but it's not working",
        "I need to dispute a charge on my account",
        "What are your business hours?"
    ]
    
    for msg in messages:
        print(f"\n👤 User: {msg}")
        result = agent.process_message(msg, auto_escalate=True)
        print(f"🤖 Agent: {result['response']}")
        if result['escalated']:
            print(f"⚠️  ESCALATED: {result['reason']}")
            break

