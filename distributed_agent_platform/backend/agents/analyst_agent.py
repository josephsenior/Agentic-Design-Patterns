from typing import Optional, List
from ..models.message import Message, MessageType
from ..models.agent import AgentType
from .base_agent import BaseAgent
from ..services.vector_service import VectorService


class AnalystAgent(BaseAgent):
    """Agent specialized in data analysis and insights."""
    
    def __init__(
        self,
        agent_id: str,
        name: str = "Analyst",
        system_message: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        vector_service: Optional[VectorService] = None
    ):
        default_system_message = """You are an analyst agent specialized in analyzing data, 
        identifying patterns, and providing insights. Your role is to:
        - Analyze provided data and information
        - Identify trends and patterns
        - Provide actionable insights
        - Create structured analysis reports
        - Highlight key findings and recommendations"""
        
        super().__init__(
            agent_id=agent_id,
            name=name,
            agent_type=AgentType.ANALYST,
            system_message=system_message or default_system_message,
            api_key=api_key,
            model=model,
            vector_service=vector_service
        )
    
    async def process_message(self, message: Message) -> Message:
        """Process an analysis request."""
        self.status = "processing"
        
        try:
            # Generate analysis
            response_content = await self.generate_response(
                f"Analyze the following: {message.content}\n\n"
                "Provide a structured analysis with key findings, patterns, and recommendations."
            )
            
            # Create response message
            response = Message(
                id=f"{message.id}_response",
                from_agent=self.agent_id,
                to_agent=message.from_agent,
                type=MessageType.RESPONSE,
                content=response_content,
                metadata={
                    "analysis_type": message.metadata.get("analysis_type", "general"),
                    "original_message_id": message.id
                },
                reply_to=message.id
            )
            
            return response
            
        finally:
            self.status = "idle"
    
    def get_capabilities(self) -> List[str]:
        """Get analyst capabilities."""
        return [
            "data_analysis",
            "pattern_recognition",
            "insights_generation",
            "report_creation"
        ]

