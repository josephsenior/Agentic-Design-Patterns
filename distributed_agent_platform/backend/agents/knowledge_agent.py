from typing import Optional, List
from ..models.message import Message, MessageType
from ..models.agent import AgentType
from .base_agent import BaseAgent
from ..services.vector_service import VectorService


class KnowledgeAgent(BaseAgent):
    """Agent specialized in knowledge management and retrieval."""
    
    def __init__(
        self,
        agent_id: str,
        name: str = "Knowledge Manager",
        system_message: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        vector_service: Optional[VectorService] = None
    ):
        if vector_service is None:
            raise ValueError("KnowledgeAgent requires a VectorService")
        
        default_system_message = """You are a knowledge management agent responsible for 
        storing, retrieving, and organizing information. Your role is to:
        - Store information in the knowledge base
        - Retrieve relevant information for queries
        - Organize and categorize knowledge
        - Provide accurate and relevant search results"""
        
        super().__init__(
            agent_id=agent_id,
            name=name,
            agent_type=AgentType.KNOWLEDGE,
            system_message=system_message or default_system_message,
            api_key=api_key,
            model=model,
            vector_service=vector_service
        )
    
    async def process_message(self, message: Message) -> Message:
        """Process a knowledge query or storage request."""
        self.status = "processing"
        
        try:
            if message.type == MessageType.QUERY:
                # Handle knowledge query
                results = await self.search_knowledge(message.content, n_results=5)
                
                if results:
                    # Format results
                    result_text = "Found the following information:\n\n"
                    for i, result in enumerate(results, 1):
                        result_text += f"{i}. {result['content']}\n"
                    
                    response_content = result_text
                else:
                    response_content = "No relevant information found in the knowledge base."
                
            else:
                # Handle knowledge storage
                doc_id = await self.add_knowledge(
                    message.content,
                    metadata=message.metadata
                )
                response_content = f"Knowledge stored successfully. ID: {doc_id}"
            
            # Create response message
            response = Message(
                id=f"{message.id}_response",
                from_agent=self.agent_id,
                to_agent=message.from_agent,
                type=MessageType.RESPONSE,
                content=response_content,
                metadata={
                    "original_message_id": message.id
                },
                reply_to=message.id
            )
            
            return response
            
        finally:
            self.status = "idle"
    
    def get_capabilities(self) -> List[str]:
        """Get knowledge agent capabilities."""
        return [
            "knowledge_storage",
            "semantic_search",
            "information_retrieval",
            "knowledge_organization"
        ]

