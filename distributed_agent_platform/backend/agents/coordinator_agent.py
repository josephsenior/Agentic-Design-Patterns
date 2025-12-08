from typing import Optional, List
from ..models.message import Message, MessageType
from ..models.agent import AgentType
from .base_agent import BaseAgent
from ..services.vector_service import VectorService


class CoordinatorAgent(BaseAgent):
    """Agent specialized in coordinating multi-agent workflows."""
    
    def __init__(
        self,
        agent_id: str,
        name: str = "Coordinator",
        system_message: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        vector_service: Optional[VectorService] = None
    ):
        default_system_message = """You are a coordinator agent responsible for orchestrating 
        multi-agent workflows. Your role is to:
        - Break down complex tasks into subtasks
        - Assign tasks to appropriate agents
        - Coordinate agent collaboration
        - Synthesize results from multiple agents
        - Ensure task completion and quality"""
        
        super().__init__(
            agent_id=agent_id,
            name=name,
            agent_type=AgentType.COORDINATOR,
            system_message=system_message or default_system_message,
            api_key=api_key,
            model=model,
            vector_service=vector_service
        )
    
    async def process_message(self, message: Message) -> Message:
        """Process a coordination request."""
        self.status = "processing"
        
        try:
            # Generate coordination plan
            response_content = await self.generate_response(
                f"Coordinate the following task: {message.content}\n\n"
                "Break down the task into subtasks and suggest which agents should handle each part."
            )
            
            # Create response message
            response = Message(
                id=f"{message.id}_response",
                from_agent=self.agent_id,
                to_agent=message.from_agent,
                type=MessageType.RESPONSE,
                content=response_content,
                metadata={
                    "coordination_plan": True,
                    "original_message_id": message.id
                },
                reply_to=message.id
            )
            
            return response
            
        finally:
            self.status = "idle"
    
    def get_capabilities(self) -> List[str]:
        """Get coordinator capabilities."""
        return [
            "task_decomposition",
            "workflow_orchestration",
            "agent_coordination",
            "result_synthesis"
        ]

