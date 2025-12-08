from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field


class AgentStatus(str, Enum):
    """Status of an agent."""
    IDLE = "idle"
    BUSY = "busy"
    PROCESSING = "processing"
    OFFLINE = "offline"
    ERROR = "error"


class AgentType(str, Enum):
    """Types of agents."""
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    COORDINATOR = "coordinator"
    KNOWLEDGE = "knowledge"
    CUSTOM = "custom"


class Agent(BaseModel):
    """Agent model."""
    
    id: str = Field(..., description="Unique agent ID")
    name: str = Field(..., description="Agent name")
    type: AgentType = Field(..., description="Agent type")
    status: AgentStatus = Field(AgentStatus.IDLE, description="Current status")
    capabilities: List[str] = Field(default_factory=list, description="Agent capabilities")
    node_id: Optional[str] = Field(None, description="Node ID where agent is running")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    last_seen: datetime = Field(default_factory=datetime.utcnow, description="Last activity timestamp")
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

