import json
from typing import Dict, Optional, Callable
from fastapi import WebSocket, WebSocketDisconnect
from ..models.message import Message


class WebSocketService:
    """WebSocket service for real-time agent communication."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.message_handlers: Dict[str, Callable] = {}
    
    async def connect(self, agent_id: str, websocket: WebSocket):
        """Connect an agent via WebSocket."""
        await websocket.accept()
        self.active_connections[agent_id] = websocket
    
    async def disconnect(self, agent_id: str):
        """Disconnect an agent."""
        if agent_id in self.active_connections:
            try:
                await self.active_connections[agent_id].close()
            except:
                pass
            del self.active_connections[agent_id]
    
    async def send_to_agent(self, agent_id: str, message: Message) -> bool:
        """Send a message to a specific agent."""
        if agent_id not in self.active_connections:
            return False
        
        try:
            websocket = self.active_connections[agent_id]
            message_data = message.dict()
            await websocket.send_json(message_data)
            return True
        except Exception as e:
            print(f"Failed to send message to {agent_id}: {e}")
            await self.disconnect(agent_id)
            return False
    
    async def broadcast(self, message: Message, exclude: Optional[str] = None):
        """Broadcast a message to all connected agents."""
        message_data = message.dict()
        disconnected = []
        
        for agent_id, websocket in self.active_connections.items():
            if agent_id == exclude:
                continue
            
            try:
                await websocket.send_json(message_data)
            except:
                disconnected.append(agent_id)
        
        # Clean up disconnected agents
        for agent_id in disconnected:
            await self.disconnect(agent_id)
    
    async def register_message_handler(self, message_type: str, handler: Callable):
        """Register a handler for specific message types."""
        self.message_handlers[message_type] = handler
    
    async def handle_message(self, agent_id: str, message_data: dict):
        """Handle incoming message from an agent."""
        message = Message(**message_data)
        message_type = message.type
        
        if message_type in self.message_handlers:
            await self.message_handlers[message_type](agent_id, message)
    
    def is_connected(self, agent_id: str) -> bool:
        """Check if an agent is connected."""
        return agent_id in self.active_connections
    
    def get_connected_agents(self) -> list[str]:
        """Get list of connected agent IDs."""
        return list(self.active_connections.keys())

