import pytest
import asyncio
from backend.agents.researcher_agent import ResearcherAgent
from backend.agents.analyst_agent import AnalystAgent
from backend.agents.coordinator_agent import CoordinatorAgent
from backend.agents.knowledge_agent import KnowledgeAgent
from backend.models.message import Message, MessageType
from backend.services.vector_service import VectorService


@pytest.fixture
async def vector_service():
    """Create a vector service for testing."""
    service = VectorService(persist_dir="./data/test_vectorstore")
    await service.initialize()
    yield service
    # Cleanup would go here


@pytest.mark.asyncio
async def test_researcher_agent(vector_service):
    """Test researcher agent."""
    agent = ResearcherAgent(
        agent_id="test_researcher",
        vector_service=vector_service
    )
    
    message = Message(
        id="test_msg_1",
        from_agent="test_sender",
        to_agent="test_researcher",
        type=MessageType.QUERY,
        content="What is artificial intelligence?"
    )
    
    response = await agent.process_message(message)
    
    assert response is not None
    assert response.from_agent == "test_researcher"
    assert response.to_agent == "test_sender"
    assert response.type == MessageType.RESPONSE
    assert len(response.content) > 0


@pytest.mark.asyncio
async def test_analyst_agent(vector_service):
    """Test analyst agent."""
    agent = AnalystAgent(
        agent_id="test_analyst",
        vector_service=vector_service
    )
    
    message = Message(
        id="test_msg_2",
        from_agent="test_sender",
        to_agent="test_analyst",
        type=MessageType.TASK,
        content="Analyze the following data: Sales increased by 20% this quarter."
    )
    
    response = await agent.process_message(message)
    
    assert response is not None
    assert response.from_agent == "test_analyst"
    assert response.type == MessageType.RESPONSE


@pytest.mark.asyncio
async def test_knowledge_agent(vector_service):
    """Test knowledge agent."""
    agent = KnowledgeAgent(
        agent_id="test_knowledge",
        vector_service=vector_service
    )
    
    # Test knowledge storage
    storage_message = Message(
        id="test_msg_3",
        from_agent="test_sender",
        to_agent="test_knowledge",
        type=MessageType.TEXT,
        content="Python is a programming language."
    )
    
    storage_response = await agent.process_message(storage_message)
    assert storage_response is not None
    assert "stored" in storage_response.content.lower()
    
    # Test knowledge retrieval
    query_message = Message(
        id="test_msg_4",
        from_agent="test_sender",
        to_agent="test_knowledge",
        type=MessageType.QUERY,
        content="What is Python?"
    )
    
    query_response = await agent.process_message(query_message)
    assert query_response is not None
    assert query_response.type == MessageType.RESPONSE


@pytest.mark.asyncio
async def test_coordinator_agent(vector_service):
    """Test coordinator agent."""
    agent = CoordinatorAgent(
        agent_id="test_coordinator",
        vector_service=vector_service
    )
    
    message = Message(
        id="test_msg_5",
        from_agent="test_sender",
        to_agent="test_coordinator",
        type=MessageType.TASK,
        content="Coordinate a research project on machine learning"
    )
    
    response = await agent.process_message(message)
    
    assert response is not None
    assert response.from_agent == "test_coordinator"
    assert response.type == MessageType.RESPONSE

