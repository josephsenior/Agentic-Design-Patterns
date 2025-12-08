from typing import Optional, List
from ..models.message import Message, MessageType
from ..models.agent import AgentType
from .base_agent import BaseAgent
from ..services.vector_service import VectorService


class ResearcherAgent(BaseAgent):
    """Agent specialized in research and information gathering."""
    
    def __init__(
        self,
        agent_id: str,
        name: str = "Researcher",
        system_message: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        vector_service: Optional[VectorService] = None
    ):
        default_system_message = """You are a research agent specialized in gathering, 
        synthesizing, and presenting information from multiple sources. Your role is to:
        - Conduct thorough research on given topics
        - Gather information from available knowledge bases
        - Synthesize findings into coherent summaries
        - Provide citations and sources when possible"""
        
        super().__init__(
            agent_id=agent_id,
            name=name,
            agent_type=AgentType.RESEARCHER,
            system_message=system_message or default_system_message,
            api_key=api_key,
            model=model,
            vector_service=vector_service
        )
    
    async def process_message(self, message: Message) -> Message:
        """Process a research request."""
        self.status = "processing"
        
        try:
            # Search knowledge base for relevant information
            knowledge_results = await self.search_knowledge(message.content, n_results=5)
            
            # Build context from knowledge base
            context_parts = []
            for result in knowledge_results:
                context_parts.append(f"- {result['content']}")
            
            context = "\n".join(context_parts) if context_parts else None
            
            # Generate research response
            response_content = await self.generate_response(
                f"Research the following topic: {message.content}",
                context=context
            )
            
            # Create response message
            response = Message(
                id=f"{message.id}_response",
                from_agent=self.agent_id,
                to_agent=message.from_agent,
                type=MessageType.RESPONSE,
                content=response_content,
                metadata={
                    "sources": len(knowledge_results),
                    "original_message_id": message.id
                },
                reply_to=message.id
            )
            
            return response
            
        finally:
            self.status = "idle"
    
    def get_capabilities(self) -> List[str]:
        """Get researcher capabilities."""
        return [
            "information_gathering",
            "research",
            "synthesis",
            "knowledge_retrieval"
        ]

