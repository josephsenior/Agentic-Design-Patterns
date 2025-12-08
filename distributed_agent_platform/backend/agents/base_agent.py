import uuid
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
import autogen
from ..models.agent import Agent, AgentType, AgentStatus
from ..models.message import Message, MessageType
from ..services.vector_service import VectorService


class BaseAgent(ABC):
    """Base class for all agents using AutoGen."""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        agent_type: AgentType,
        system_message: str,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        temperature: float = 0.7,
        vector_service: Optional[VectorService] = None
    ):
        self.agent_id = agent_id
        self.name = name
        self.agent_type = agent_type
        self.system_message = system_message
        self.model = model
        self.temperature = temperature
        self.vector_service = vector_service
        self.status = AgentStatus.IDLE
        
        # Initialize AutoGen agent
        api_key_value = api_key or self._get_api_key()
        model_to_use = model
        
        # Check if OpenRouter should be used
        import os
        use_openrouter = os.getenv("USE_OPENROUTER", "false").lower() == "true"
        
        if use_openrouter:
            openrouter_key = os.getenv("OPENROUTER_API_KEY")
            openrouter_model = os.getenv("OPENROUTER_MODEL", "tngtech/deepseek-r1t2-chimera:free")
            if openrouter_key:
                api_key_value = openrouter_key
                model_to_use = openrouter_model
                config_list = [
                    {
                        "model": model_to_use,
                        "api_key": api_key_value,
                        "base_url": "https://openrouter.ai/api/v1",
                    }
                ]
            else:
                config_list = [
                    {
                        "model": model,
                        "api_key": api_key_value,
                    }
                ]
        else:
            config_list = [
                {
                    "model": model,
                    "api_key": api_key_value,
                }
            ]
        
        llm_config = {
            "config_list": config_list,
            "temperature": temperature,
        }
        
        self.autogen_agent = autogen.AssistantAgent(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
        )
    
    def _get_api_key(self) -> str:
        """Get API key from environment."""
        import os
        use_openrouter = os.getenv("USE_OPENROUTER", "false").lower() == "true"
        if use_openrouter:
            return os.getenv("OPENROUTER_API_KEY", os.getenv("OPENAI_API_KEY", ""))
        return os.getenv("OPENAI_API_KEY", "")
    
    @abstractmethod
    async def process_message(self, message: Message) -> Message:
        """Process an incoming message and return a response."""
        pass
    
    async def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate a response using the AutoGen agent."""
        if context:
            full_prompt = f"Context: {context}\n\nUser: {prompt}"
        else:
            full_prompt = prompt
        
        # Use AutoGen's chat method
        response = self.autogen_agent.generate_reply(
            messages=[{"role": "user", "content": full_prompt}]
        )
        
        return response if isinstance(response, str) else str(response)
    
    async def search_knowledge(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search the knowledge base."""
        if not self.vector_service:
            return []
        
        return await self.vector_service.search(query, n_results=n_results)
    
    async def add_knowledge(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add knowledge to the vector store."""
        if not self.vector_service:
            return ""
        
        return await self.vector_service.add_knowledge(content, metadata)
    
    def to_agent_model(self, node_id: Optional[str] = None) -> Agent:
        """Convert to Agent model."""
        return Agent(
            id=self.agent_id,
            name=self.name,
            type=self.agent_type,
            status=self.status,
            capabilities=self.get_capabilities(),
            node_id=node_id,
            metadata={}
        )
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities."""
        pass

