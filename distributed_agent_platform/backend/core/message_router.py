import uuid
from typing import Optional, List, Dict
from ..models.message import Message, MessageType
from ..models.agent import Agent, AgentType, AgentStatus
from .agent_manager import AgentManager


class MessageRouter:
    """Routes messages to appropriate agents based on content and capabilities."""
    
    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
    
    async def route_message(
        self,
        message: Message
    ) -> List[str]:
        """Route a message to appropriate agent(s)."""
        # Direct routing if to_agent is specified
        if message.to_agent:
            agent = await self.agent_manager.get_agent(message.to_agent)
            if agent and agent.status != AgentStatus.OFFLINE:
                return [message.to_agent]
            return []
        
        # Broadcast routing
        if message.type == MessageType.BROADCAST:
            agents = await self.agent_manager.list_agents(
                status=AgentStatus.IDLE
            )
            return [a.id for a in agents]
        
        # Content-based routing
        if message.type == MessageType.QUERY:
            return await self._route_query(message)
        elif message.type == MessageType.TASK:
            return await self._route_task(message)
        else:
            # Default: route to coordinator or first available agent
            return await self._route_default(message)
    
    async def _route_query(self, message: Message) -> List[str]:
        """Route query messages to knowledge or researcher agents."""
        agents = await self.agent_manager.list_agents(
            status=AgentStatus.IDLE
        )
        
        # Prefer knowledge agents for queries
        knowledge_agents = [a for a in agents if a.type == AgentType.KNOWLEDGE]
        if knowledge_agents:
            return [knowledge_agents[0].id]
        
        # Fallback to researcher agents
        researcher_agents = [a for a in agents if a.type == AgentType.RESEARCHER]
        if researcher_agents:
            return [researcher_agents[0].id]
        
        return []
    
    async def _route_task(self, message: Message) -> List[str]:
        """Route task messages based on task type in metadata."""
        task_type = message.metadata.get("task_type", "").lower()
        
        agents = await self.agent_manager.list_agents(
            status=AgentStatus.IDLE
        )
        
        # Route based on task type
        if "analysis" in task_type or "analyze" in task_type:
            analyst_agents = [a for a in agents if a.type == AgentType.ANALYST]
            if analyst_agents:
                return [analyst_agents[0].id]
        
        if "research" in task_type or "gather" in task_type:
            researcher_agents = [a for a in agents if a.type == AgentType.RESEARCHER]
            if researcher_agents:
                return [researcher_agents[0].id]
        
        # Default: route to coordinator
        coordinator_agents = [a for a in agents if a.type == AgentType.COORDINATOR]
        if coordinator_agents:
            return [coordinator_agents[0].id]
        
        # Fallback to first available agent
        if agents:
            return [agents[0].id]
        
        return []
    
    async def _route_default(self, message: Message) -> List[str]:
        """Default routing logic."""
        agents = await self.agent_manager.list_agents(
            status=AgentStatus.IDLE
        )
        
        # Prefer coordinator for general messages
        coordinator_agents = [a for a in agents if a.type == AgentType.COORDINATOR]
        if coordinator_agents:
            return [coordinator_agents[0].id]
        
        # Fallback to first available agent
        if agents:
            return [agents[0].id]
        
        return []

