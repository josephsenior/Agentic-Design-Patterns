# Distributed Multi-Agent Communication Platform

A production-ready distributed system for multi-agent communication, collaboration, and knowledge sharing. Built with AutoGen, featuring real-time WebSocket communication, production vector database integration, and intelligent agent routing.

## Features

### Core Capabilities

- **Distributed Agent Architecture**: Multiple agents running across different nodes with automatic discovery
- **Real-Time Communication**: WebSocket-based agent-to-agent messaging
- **Production Vector Database**: ChromaDB integration for semantic search and knowledge retrieval
- **Message Queue System**: Redis-based message queuing for reliable agent communication
- **Agent Discovery & Routing**: Automatic agent discovery and intelligent message routing
- **Load Balancing**: Distribute agent workloads across available nodes
- **Knowledge Sharing**: Agents can share and retrieve knowledge from a shared vector store
- **Monitoring Dashboard**: Real-time monitoring of agent activities and system health

### Agent Types

- **Researcher Agent**: Gathers and synthesizes information from multiple sources
- **Analyst Agent**: Performs deep analysis on provided data
- **Coordinator Agent**: Orchestrates multi-agent workflows
- **Knowledge Agent**: Manages and retrieves information from the vector database

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Agent Node 1  │     │   Agent Node 2  │     │   Agent Node 3  │
│                 │     │                 │     │                 │
│  ┌───────────┐  │     │  ┌───────────┐  │     │  ┌───────────┐  │
│  │ Researcher│  │     │  │  Analyst  │  │     │  │Coordinator│  │
│  └─────┬─────┘  │     │  └─────┬─────┘  │     │  └─────┬─────┘  │
│        │        │     │        │        │     │        │        │
└────────┼────────┘     └────────┼────────┘     └────────┼────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
            ┌───────▼────────┐      ┌────────▼────────┐
            │  Redis Queue   │      │   ChromaDB      │
            │  (Messaging)   │      │  (Knowledge)    │
            └────────────────┘      └─────────────────┘
                    │                         │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   API Gateway           │
                    │   (FastAPI + WebSocket) │
                    └─────────────────────────┘
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd distributed_agent_platform

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Start Redis (if not running)
# On macOS with Homebrew:
brew services start redis
# On Linux:
sudo systemctl start redis
# On Windows, download and run Redis

# Run the platform
python main.py
```

## Quick Start

### 1. Start the Platform

```bash
python main.py
```

This will start:
- FastAPI server on `http://localhost:8000`
- WebSocket server on `ws://localhost:8001`
- Agent discovery service
- Vector database service

### 2. Access the Dashboard

Open your browser to `http://localhost:8000` to access the monitoring dashboard.

### 3. Create Agents

```python
from backend.agents.researcher_agent import ResearcherAgent
from backend.core.agent_manager import AgentManager

# Initialize agent manager
manager = AgentManager()

# Create a researcher agent
researcher = ResearcherAgent(
    name="researcher_1",
    system_message="You are a research agent specialized in gathering information."
)

# Register agent
manager.register_agent(researcher)
```

### 4. Send Messages Between Agents

```python
# Send a message from one agent to another
message = {
    "from": "researcher_1",
    "to": "analyst_1",
    "content": "Please analyze this data: ...",
    "type": "analysis_request"
}

manager.send_message(message)
```

## Project Structure

```
distributed_agent_platform/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py          # Base agent class
│   │   ├── researcher_agent.py    # Researcher agent implementation
│   │   ├── analyst_agent.py       # Analyst agent implementation
│   │   ├── coordinator_agent.py   # Coordinator agent implementation
│   │   └── knowledge_agent.py     # Knowledge management agent
│   ├── core/
│   │   ├── __init__.py
│   │   ├── agent_manager.py       # Agent lifecycle management
│   │   ├── message_router.py      # Message routing logic
│   │   ├── discovery_service.py   # Agent discovery
│   │   └── load_balancer.py       # Load balancing
│   ├── services/
│   │   ├── __init__.py
│   │   ├── vector_service.py      # ChromaDB integration
│   │   ├── queue_service.py       # Redis queue management
│   │   └── websocket_service.py   # WebSocket communication
│   └── models/
│       ├── __init__.py
│       ├── message.py             # Message models
│       └── agent.py               # Agent models
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       └── index.html             # Dashboard UI
├── tests/
│   ├── test_agents.py
│   ├── test_routing.py
│   └── test_vector_service.py
├── main.py                        # Application entry point
├── requirements.txt
└── README.md
```

## API Endpoints

### REST API

- `GET /health` - Health check
- `GET /agents` - List all registered agents
- `POST /agents/register` - Register a new agent
- `DELETE /agents/{agent_id}` - Unregister an agent
- `POST /messages/send` - Send a message between agents
- `GET /messages/{agent_id}` - Get messages for an agent
- `GET /metrics` - System metrics

### WebSocket API

- `ws://localhost:8001/ws/{agent_id}` - Agent WebSocket connection
- Messages: `{"type": "message", "to": "agent_id", "content": "..."}`

## Configuration

Edit `.env` to configure:

- **OpenAI API**: Set your API key
- **Redis**: Configure Redis connection
- **ChromaDB**: Set persistence directory
- **Server**: Configure host and ports
- **Agents**: Set limits and timeouts

## Monitoring

The platform includes built-in monitoring:

- Agent status and health
- Message throughput
- Queue depth
- Vector database statistics
- System resource usage

Access the dashboard at `http://localhost:8000` for real-time monitoring.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_agents.py
```

## License

MIT License

