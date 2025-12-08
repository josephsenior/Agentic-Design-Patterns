from typing import List, Optional
from ..models.agent import Agent, AgentStatus, AgentType
from .agent_manager import AgentManager


class LoadBalancer:
    """Load balancer for distributing work across agents."""
    
    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
    
    async def select_agent(
        self,
        agent_type: Optional[AgentType] = None,
        strategy: str = "round_robin"
    ) -> Optional[Agent]:
        """Select an agent using the specified strategy."""
        agents = await self.agent_manager.list_agents(
            agent_type=agent_type,
            status=AgentStatus.IDLE
        )
        
        if not agents:
            # Fallback to busy agents if no idle agents
            agents = await self.agent_manager.list_agents(agent_type=agent_type)
            agents = [a for a in agents if a.status != AgentStatus.OFFLINE]
        
        if not agents:
            return None
        
        if strategy == "round_robin":
            return await self._round_robin(agents)
        elif strategy == "least_busy":
            return await self._least_busy(agents)
        elif strategy == "random":
            import random
            return random.choice(agents)
        else:
            return agents[0]
    
    async def _round_robin(self, agents: List[Agent]) -> Agent:
        """Round-robin selection."""
        # Simple round-robin based on agent ID
        # In production, you'd maintain state for true round-robin
        return agents[0]
    
    async def _least_busy(self, agents: List[Agent]) -> Agent:
        """Select the least busy agent."""
        # For now, prefer idle agents
        idle_agents = [a for a in agents if a.status == AgentStatus.IDLE]
        if idle_agents:
            return idle_agents[0]
        return agents[0]

