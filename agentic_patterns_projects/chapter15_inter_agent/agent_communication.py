"""
Inter-Agent Communication - Inter-Agent Communication Pattern

This module implements communication protocols for agents to interact
and share information with each other.
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class AgentMessage:
    """Represents a message between agents."""
    
    def __init__(self, sender: str, receiver: str, content: str, message_type: str = "request"):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.message_type = message_type  # "request", "response", "notification"
        self.timestamp = "now"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "type": self.message_type,
            "timestamp": self.timestamp
        }


class CommunicatingAgent:
    """
    An agent that can send and receive messages from other agents.
    """
    
    def __init__(
        self,
        agent_id: str,
        role: str,
        llm: ChatOpenAI
    ):
        """Initialize a communicating agent."""
        self.agent_id = agent_id
        self.role = role
        self.llm = llm
        self.inbox = []
        self.outbox = []
        self._build_agent()
    
    def _build_agent(self):
        """Build the agent's communication chain."""
        
        self.response_prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are {self.role}. You can communicate with other agents 
to accomplish tasks. When you receive a message, respond appropriately based on your role."""),
            ("user", """Message from {sender}: {message}
Your role: {role}
Respond to this message.""")
        ])
        
        self.response_chain = self.response_prompt | self.llm | StrOutputParser()
    
    def receive_message(self, message: AgentMessage):
        """Receive a message from another agent."""
        self.inbox.append(message)
        print(f"📨 [{self.agent_id}] Received message from {message.sender}")
    
    def process_message(self, message: AgentMessage) -> AgentMessage:
        """
        Process a received message and generate a response.
        
        Args:
            message: The received message
            
        Returns:
            Response message
        """
        response_content = self.response_chain.invoke({
            "sender": message.sender,
            "message": message.content,
            "role": self.role
        })
        
        response = AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            content=response_content,
            message_type="response"
        )
        
        self.outbox.append(response)
        return response
    
    def send_message(self, receiver: str, content: str) -> AgentMessage:
        """Create and send a message to another agent."""
        message = AgentMessage(
            sender=self.agent_id,
            receiver=receiver,
            content=content,
            message_type="request"
        )
        self.outbox.append(message)
        return message


class AgentCommunicationHub:
    """
    A hub that manages communication between multiple agents.
    """
    
    def __init__(self):
        self.agents = {}
        self.message_queue = []
    
    def register_agent(self, agent: CommunicatingAgent):
        """Register an agent in the communication hub."""
        self.agents[agent.agent_id] = agent
        print(f"✅ Registered agent: {agent.agent_id} ({agent.role})")
    
    def send_message(self, sender_id: str, receiver_id: str, content: str):
        """Send a message from one agent to another."""
        if receiver_id not in self.agents:
            raise ValueError(f"Agent {receiver_id} not found")
        
        sender = self.agents[sender_id]
        receiver = self.agents[receiver_id]
        
        message = sender.send_message(receiver_id, content)
        receiver.receive_message(message)
        
        # Process and respond
        response = receiver.process_message(message)
        sender.receive_message(response)
        
        return {
            "request": message.to_dict(),
            "response": response.to_dict()
        }
    
    def broadcast(self, sender_id: str, content: str):
        """Broadcast a message to all agents."""
        sender = self.agents[sender_id]
        responses = []
        
        for agent_id, agent in self.agents.items():
            if agent_id != sender_id:
                result = self.send_message(sender_id, agent_id, content)
                responses.append(result)
        
        return responses


if __name__ == "__main__":
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI()
    
    print("=" * 70)
    print("INTER-AGENT COMMUNICATION - AGENT COMMUNICATION PATTERN")
    print("=" * 70)
    
    # Create agents
    researcher = CommunicatingAgent("researcher", "Research Specialist", llm)
    writer = CommunicatingAgent("writer", "Content Writer", llm)
    editor = CommunicatingAgent("editor", "Editor", llm)
    
    # Create hub
    hub = AgentCommunicationHub()
    hub.register_agent(researcher)
    hub.register_agent(writer)
    hub.register_agent(editor)
    
    # Test communication
    print("\n📡 Testing agent communication...")
    result = hub.send_message(
        "researcher",
        "writer",
        "I found that AI is transforming healthcare. Can you write about this?"
    )
    
    print(f"\n💬 Request: {result['request']['content']}")
    print(f"💬 Response: {result['response']['content'][:100]}...")

