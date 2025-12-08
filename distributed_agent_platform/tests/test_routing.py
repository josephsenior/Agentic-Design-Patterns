import pytest
from backend.core.agent_manager import AgentManager
from backend.core.message_router import MessageRouter
from backend.models.agent import AgentType, AgentStatus
from backend.models.message import Message, MessageType


@pytest.mark.asyncio
async def test_message_routing():
    """Test message routing."""
    agent_manager = AgentManager()
    router = MessageRouter(agent_manager)
    
    # Register some agents
    await agent_manager.register_agent(
        "researcher_1",
        "Researcher",
        AgentType.RESEARCHER,
        ["research"]
    )
    
    await agent_manager.register_agent(
        "analyst_1",
        "Analyst",
        AgentType.ANALYST,
        ["analysis"]
    )
    
    # Test direct routing
    message = Message(
        id="msg_1",
        from_agent="sender",
        to_agent="researcher_1",
        type=MessageType.TEXT,
        content="Test message"
    )
    
    targets = await router.route_message(message)
    assert "researcher_1" in targets
    
    # Test query routing (should route to knowledge/researcher)
    query_message = Message(
        id="msg_2",
        from_agent="sender",
        to_agent=None,
        type=MessageType.QUERY,
        content="What is AI?"
    )
    
    targets = await router.route_message(query_message)
    assert len(targets) > 0

