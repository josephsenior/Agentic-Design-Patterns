import json
import asyncio
from typing import Optional, Callable, Dict, Any
import redis.asyncio as redis
from ..models.message import Message
import os
from dotenv import load_dotenv

load_dotenv()


class QueueService:
    """Redis-based message queue service."""
    
    def __init__(
        self,
        host: Optional[str] = None,
        port: int = 6379,
        db: int = 0
    ):
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", 6379))
        self.db = db or int(os.getenv("REDIS_DB", 0))
        self.redis_client: Optional[redis.Redis] = None
        self._agent_event_callbacks: list[Callable] = []
    
    async def connect(self):
        """Connect to Redis."""
        try:
            self.redis_client = await redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True
            )
            await self.redis_client.ping()
        except Exception as e:
            print(f"Failed to connect to Redis: {e}")
            # Fallback to in-memory queue if Redis is not available
            self.redis_client = None
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self.redis_client:
            await self.redis_client.close()
    
    async def enqueue_message(self, message: Message, queue_name: str = "messages"):
        """Enqueue a message."""
        if not self.redis_client:
            return
        
        message_data = message.dict()
        message_json = json.dumps(message_data)
        
        if message.to_agent:
            # Use agent-specific queue
            agent_queue = f"{queue_name}:{message.to_agent}"
            await self.redis_client.lpush(agent_queue, message_json)
        else:
            # Use general queue
            await self.redis_client.lpush(queue_name, message_json)
    
    async def dequeue_message(
        self,
        agent_id: Optional[str] = None,
        queue_name: str = "messages",
        timeout: int = 1
    ) -> Optional[Message]:
        """Dequeue a message."""
        if not self.redis_client:
            return None
        
        if agent_id:
            agent_queue = f"{queue_name}:{agent_id}"
            result = await self.redis_client.brpop(agent_queue, timeout=timeout)
        else:
            result = await self.redis_client.brpop(queue_name, timeout=timeout)
        
        if result:
            _, message_json = result
            message_data = json.loads(message_json)
            return Message(**message_data)
        
        return None
    
    async def publish_agent_event(self, event_type: str, agent_data: Dict[str, Any]):
        """Publish an agent event."""
        if not self.redis_client:
            # Call callbacks directly if Redis is not available
            for callback in self._agent_event_callbacks:
                await callback(event_type, agent_data)
            return
        
        event_data = {
            "type": event_type,
            "agent": agent_data
        }
        event_json = json.dumps(event_data)
        await self.redis_client.publish("agent_events", event_json)
    
    async def subscribe_agent_events(self, callback: Callable):
        """Subscribe to agent events."""
        self._agent_event_callbacks.append(callback)
        
        if not self.redis_client:
            return
        
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe("agent_events")
        
        async def listen():
            async for message in pubsub.listen():
                if message["type"] == "message":
                    event_data = json.loads(message["data"])
                    await callback(event_data["type"], event_data["agent"])
        
        asyncio.create_task(listen())

