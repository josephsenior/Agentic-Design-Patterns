import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from ..models.agent import Agent
from ..services.queue_service import QueueService


class DiscoveryService:
    """Service for discovering agents across distributed nodes."""
    
    def __init__(self, queue_service: QueueService):
        self.queue_service = queue_service
        self.discovered_agents: Dict[str, Agent] = {}
        self.node_registry: Dict[str, Dict] = {}
        self._discovery_interval = 10  # seconds
        self._node_timeout = 30  # seconds
    
    async def start_discovery(self):
        """Start the discovery service."""
        # Subscribe to agent events
        await self.queue_service.subscribe_agent_events(self._handle_agent_event)
        
        # Start periodic discovery
        asyncio.create_task(self._periodic_discovery())
    
    async def _handle_agent_event(self, event_type: str, agent_data: Dict):
        """Handle agent events from the queue."""
        agent = Agent(**agent_data)
        
        if event_type == "registered":
            self.discovered_agents[agent.id] = agent
            if agent.node_id:
                if agent.node_id not in self.node_registry:
                    self.node_registry[agent.node_id] = {
                        "agents": [],
                        "last_seen": datetime.utcnow()
                    }
                if agent.id not in self.node_registry[agent.node_id]["agents"]:
                    self.node_registry[agent.node_id]["agents"].append(agent.id)
                self.node_registry[agent.node_id]["last_seen"] = datetime.utcnow()
        
        elif event_type == "unregistered":
            if agent.id in self.discovered_agents:
                del self.discovered_agents[agent.id]
            if agent.node_id and agent.node_id in self.node_registry:
                if agent.id in self.node_registry[agent.node_id]["agents"]:
                    self.node_registry[agent.node_id]["agents"].remove(agent.id)
        
        elif event_type == "offline":
            if agent.id in self.discovered_agents:
                self.discovered_agents[agent.id].status = agent.status
    
    async def _periodic_discovery(self):
        """Periodic discovery and cleanup."""
        while True:
            await asyncio.sleep(self._discovery_interval)
            await self._cleanup_stale_nodes()
    
    async def _cleanup_stale_nodes(self):
        """Remove nodes that haven't been seen recently."""
        now = datetime.utcnow()
        timeout = timedelta(seconds=self._node_timeout)
        
        stale_nodes = []
        for node_id, node_info in list(self.node_registry.items()):
            if now - node_info["last_seen"] > timeout:
                stale_nodes.append(node_id)
        
        for node_id in stale_nodes:
            # Mark all agents from this node as offline
            for agent_id in self.node_registry[node_id]["agents"]:
                if agent_id in self.discovered_agents:
                    self.discovered_agents[agent_id].status = "offline"
            del self.node_registry[node_id]
    
    async def discover_agents(
        self,
        agent_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Agent]:
        """Discover agents matching criteria."""
        agents = list(self.discovered_agents.values())
        
        if agent_type:
            agents = [a for a in agents if a.type == agent_type]
        
        if status:
            agents = [a for a in agents if a.status == status]
        
        return agents
    
    async def get_node_info(self, node_id: str) -> Optional[Dict]:
        """Get information about a specific node."""
        return self.node_registry.get(node_id)

