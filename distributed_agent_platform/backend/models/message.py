from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class MessageType(str, Enum):
    """Types of messages between agents."""
    TEXT = "text"
    QUERY = "query"
    RESPONSE = "response"
    TASK = "task"
    RESULT = "result"
    BROADCAST = "broadcast"
    HEARTBEAT = "heartbeat"


class MessageStatus(str, Enum):
    """Status of a message."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    PROCESSED = "processed"
    FAILED = "failed"


class Message(BaseModel):
    """Message model for agent communication."""
    
    id: str = Field(..., description="Unique message ID")
    from_agent: str = Field(..., description="Sender agent ID")
    to_agent: Optional[str] = Field(None, description="Recipient agent ID (None for broadcast)")
    type: MessageType = Field(MessageType.TEXT, description="Message type")
    content: str = Field(..., description="Message content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    status: MessageStatus = Field(MessageStatus.PENDING, description="Message status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")
    reply_to: Optional[str] = Field(None, description="ID of message this is replying to")
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

