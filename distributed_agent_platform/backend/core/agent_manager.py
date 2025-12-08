import asyncio
import uuid
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from ..models.agent import Agent, AgentStatus, AgentType
from ..models.message import Message, MessageType, MessageStatus
from ..services.queue_service import QueueService
from ..services.websocket_service import WebSocketService


class AgentManager:
    """Manages agent lifecycle and communication."""
    
    def __init__(
        self,
        queue_service: Optional[QueueService] = None,
        websocket_service: Optional[WebSocketService] = None,
        node_id: Optional[str] = None
    ):
        self.agents: Dict[str, Agent] = {}
        self.queue_service = queue_service
        self.websocket_service = websocket_service
        self.node_id = node_id or str(uuid.uuid4())
        self._heartbeat_interval = 30  # seconds
        
    async def register_agent(
        self,
        agent_id: str,
        name: str,
        agent_type: AgentType,
        capabilities: List[str] = None,
        metadata: Dict = None
    ) -> Agent:
        """Register a new agent."""
        agent = Agent(
            id=agent_id,
            name=name,
            type=agent_type,
            status=AgentStatus.IDLE,
            capabilities=capabilities or [],
            node_id=self.node_id,
            metadata=metadata or {}
        )
        
        self.agents[agent_id] = agent
        
        # Notify other services
        if self.queue_service:
            await self.queue_service.publish_agent_event("registered", agent.dict())
        
        return agent
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        agent.status = AgentStatus.OFFLINE
        
        # Notify other services
        if self.queue_service:
            await self.queue_service.publish_agent_event("unregistered", agent.dict())
        
        del self.agents[agent_id]
        return True
    
    async def update_agent_status(
        self,
        agent_id: str,
        status: AgentStatus
    ) -> bool:
        """Update agent status."""
        if agent_id not in self.agents:
            return False
        
        self.agents[agent_id].status = status
        self.agents[agent_id].last_seen = datetime.utcnow()
        return True
    
    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID."""
        return self.agents.get(agent_id)
    
    async def list_agents(
        self,
        agent_type: Optional[AgentType] = None,
        status: Optional[AgentStatus] = None
    ) -> List[Agent]:
        """List all agents with optional filtering."""
        agents = list(self.agents.values())
        
        if agent_type:
            agents = [a for a in agents if a.type == agent_type]
        
        if status:
            agents = [a for a in agents if a.status == status]
        
        return agents
    
    async def send_message(
        self,
        from_agent: str,
        to_agent: Optional[str],
        content: str,
        message_type: MessageType = MessageType.TEXT,
        metadata: Dict = None
    ) -> Message:
        """Send a message between agents."""
        message = Message(
            id=str(uuid.uuid4()),
            from_agent=from_agent,
            to_agent=to_agent,
            type=message_type,
            content=content,
            metadata=metadata or {},
            status=MessageStatus.PENDING
        )
        
        # Try direct WebSocket delivery first
        if to_agent and self.websocket_service:
            delivered = await self.websocket_service.send_to_agent(to_agent, message)
            if delivered:
                message.status = MessageStatus.DELIVERED
                return message
        
        # Fallback to queue
        if self.queue_service:
            await self.queue_service.enqueue_message(message)
            message.status = MessageStatus.SENT
        
        return message
    
    async def start_heartbeat(self):
        """Start heartbeat monitoring for agents."""
        while True:
            await asyncio.sleep(self._heartbeat_interval)
            await self._check_agent_health()
    
    async def _check_agent_health(self):
        """Check agent health and mark offline if needed."""
        now = datetime.utcnow()
        timeout = timedelta(seconds=self._heartbeat_interval * 3)
        
        for agent_id, agent in list(self.agents.items()):
            if agent.status != AgentStatus.OFFLINE:
                if now - agent.last_seen > timeout:
                    agent.status = AgentStatus.OFFLINE
                    if self.queue_service:
                        await self.queue_service.publish_agent_event("offline", agent.dict())

