import asyncio
import os
import uuid
from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from backend.core.agent_manager import AgentManager
from backend.core.message_router import MessageRouter
from backend.core.discovery_service import DiscoveryService
from backend.core.load_balancer import LoadBalancer
from backend.services.queue_service import QueueService
from backend.services.websocket_service import WebSocketService
from backend.services.vector_service import VectorService
from backend.agents.researcher_agent import ResearcherAgent
from backend.agents.analyst_agent import AnalystAgent
from backend.agents.coordinator_agent import CoordinatorAgent
from backend.agents.knowledge_agent import KnowledgeAgent
from backend.models.agent import Agent, AgentType, AgentStatus
from backend.models.message import Message, MessageType

load_dotenv()

# Global services
queue_service: Optional[QueueService] = None
websocket_service: Optional[WebSocketService] = None
vector_service: Optional[VectorService] = None
agent_manager: Optional[AgentManager] = None
message_router: Optional[MessageRouter] = None
discovery_service: Optional[DiscoveryService] = None
load_balancer: Optional[LoadBalancer] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global queue_service, websocket_service, vector_service
    global agent_manager, message_router, discovery_service, load_balancer
    
    # Initialize services
    queue_service = QueueService()
    await queue_service.connect()
    
    websocket_service = WebSocketService()
    
    vector_service = VectorService()
    await vector_service.initialize()
    
    # Initialize core components
    agent_manager = AgentManager(
        queue_service=queue_service,
        websocket_service=websocket_service
    )
    
    message_router = MessageRouter(agent_manager)
    load_balancer = LoadBalancer(agent_manager)
    
    discovery_service = DiscoveryService(queue_service)
    await discovery_service.start_discovery()
    
    # Start background tasks
    asyncio.create_task(agent_manager.start_heartbeat())
    asyncio.create_task(message_processor())
    
    # Create default agents
    await create_default_agents()
    
    yield
    
    # Cleanup
    if queue_service:
        await queue_service.disconnect()


app = FastAPI(
    title="Distributed Multi-Agent Communication Platform",
    description="Production-ready distributed system for multi-agent communication",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


# Pydantic models for API
class AgentCreate(BaseModel):
    name: str
    agent_type: AgentType
    capabilities: Optional[List[str]] = None
    metadata: Optional[dict] = None


class MessageSend(BaseModel):
    from_agent: str
    to_agent: Optional[str] = None
    content: str
    message_type: MessageType = MessageType.TEXT
    metadata: Optional[dict] = None


async def create_default_agents():
    """Create default agents on startup."""
    if not agent_manager or not vector_service:
        return
    
    # Create researcher agent
    researcher = ResearcherAgent(
        agent_id="researcher_1",
        name="Researcher",
        vector_service=vector_service
    )
    await agent_manager.register_agent(
        researcher.agent_id,
        researcher.name,
        AgentType.RESEARCHER,
        researcher.get_capabilities()
    )
    
    # Create analyst agent
    analyst = AnalystAgent(
        agent_id="analyst_1",
        name="Analyst",
        vector_service=vector_service
    )
    await agent_manager.register_agent(
        analyst.agent_id,
        analyst.name,
        AgentType.ANALYST,
        analyst.get_capabilities()
    )
    
    # Create coordinator agent
    coordinator = CoordinatorAgent(
        agent_id="coordinator_1",
        name="Coordinator",
        vector_service=vector_service
    )
    await agent_manager.register_agent(
        coordinator.agent_id,
        coordinator.name,
        AgentType.COORDINATOR,
        coordinator.get_capabilities()
    )
    
    # Create knowledge agent
    knowledge = KnowledgeAgent(
        agent_id="knowledge_1",
        name="Knowledge Manager",
        vector_service=vector_service
    )
    await agent_manager.register_agent(
        knowledge.agent_id,
        knowledge.name,
        AgentType.KNOWLEDGE,
        knowledge.get_capabilities()
    )


async def message_processor():
    """Background task to process messages from queue."""
    while True:
        try:
            if queue_service:
                message = await queue_service.dequeue_message(timeout=1)
                if message and agent_manager:
                    # Route message
                    target_agents = await message_router.route_message(message)
                    
                    # Send to target agents
                    for agent_id in target_agents:
                        if websocket_service:
                            await websocket_service.send_to_agent(agent_id, message)
        except Exception as e:
            print(f"Error processing message: {e}")
        
        await asyncio.sleep(0.1)


@app.get("/")
async def read_root():
    """Serve the dashboard."""
    with open("frontend/templates/index.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agents": len(agent_manager.agents) if agent_manager else 0,
        "connected_websockets": len(websocket_service.active_connections) if websocket_service else 0
    }


@app.get("/agents", response_model=List[Agent])
async def list_agents(
    agent_type: Optional[AgentType] = None,
    status: Optional[AgentStatus] = None
):
    """List all agents."""
    if not agent_manager:
        return []
    
    return await agent_manager.list_agents(agent_type, status)


@app.post("/agents/register", response_model=Agent)
async def register_agent(agent_data: AgentCreate):
    """Register a new agent."""
    if not agent_manager:
        raise HTTPException(status_code=500, detail="Agent manager not initialized")
    
    agent_id = str(uuid.uuid4())
    agent = await agent_manager.register_agent(
        agent_id=agent_id,
        name=agent_data.name,
        agent_type=agent_data.agent_type,
        capabilities=agent_data.capabilities or [],
        metadata=agent_data.metadata or {}
    )
    
    return agent


@app.delete("/agents/{agent_id}")
async def unregister_agent(agent_id: str):
    """Unregister an agent."""
    if not agent_manager:
        raise HTTPException(status_code=500, detail="Agent manager not initialized")
    
    success = await agent_manager.unregister_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {"message": "Agent unregistered"}


@app.post("/messages/send", response_model=Message)
async def send_message(message_data: MessageSend):
    """Send a message between agents."""
    if not agent_manager:
        raise HTTPException(status_code=500, detail="Agent manager not initialized")
    
    message = await agent_manager.send_message(
        from_agent=message_data.from_agent,
        to_agent=message_data.to_agent,
        content=message_data.content,
        message_type=message_data.message_type,
        metadata=message_data.metadata or {}
    )
    
    return message


@app.get("/metrics")
async def get_metrics():
    """Get system metrics."""
    stats = {}
    
    if vector_service:
        stats["vector_db"] = await vector_service.get_collection_stats()
    
    if agent_manager:
        stats["agents"] = {
            "total": len(agent_manager.agents),
            "by_status": {},
            "by_type": {}
        }
        for agent in agent_manager.agents.values():
            stats["agents"]["by_status"][agent.status] = \
                stats["agents"]["by_status"].get(agent.status, 0) + 1
            stats["agents"]["by_type"][agent.type] = \
                stats["agents"]["by_type"].get(agent.type, 0) + 1
    
    if websocket_service:
        stats["websockets"] = {
            "connected": len(websocket_service.active_connections)
        }
    
    return stats


@app.websocket("/ws/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    """WebSocket endpoint for agent communication."""
    if not websocket_service:
        await websocket.close(code=1011, reason="WebSocket service not initialized")
        return
    
    await websocket_service.connect(agent_id, websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            await websocket_service.handle_message(agent_id, data)
    except WebSocketDisconnect:
        await websocket_service.disconnect(agent_id)


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", 8000))
    
    uvicorn.run(app, host=host, port=port)

