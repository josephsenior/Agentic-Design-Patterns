# Quick Start Guide

Get up and running with the Distributed Multi-Agent Communication Platform in minutes.

## Prerequisites

- Python 3.9 or higher
- Redis (optional, but recommended)
- OpenAI API key

## Installation

### 1. Clone and Install

```bash
# Navigate to project directory
cd distributed_agent_platform

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your-key-here
```

### 3. Start Redis (Optional)

If you have Redis installed:

```bash
# macOS (Homebrew)
brew services start redis

# Linux
sudo systemctl start redis

# Windows
# Download and run Redis from https://redis.io/download
```

If Redis is not available, the system will fall back to in-memory queues.

### 4. Run the Platform

```bash
python main.py
```

The platform will start on `http://localhost:8000`

## Using the Platform

### Access the Dashboard

Open your browser to `http://localhost:8000` to access the web dashboard.

### Default Agents

The platform automatically creates four default agents on startup:

- **Researcher Agent** (`researcher_1`): Specialized in information gathering
- **Analyst Agent** (`analyst_1`): Performs data analysis
- **Coordinator Agent** (`coordinator_1`): Orchestrates workflows
- **Knowledge Agent** (`knowledge_1`): Manages knowledge base

### Send a Message

Using the dashboard:

1. Enter "researcher_1" in "From Agent ID"
2. Enter "knowledge_1" in "To Agent ID"
3. Select "Query" as message type
4. Enter your query: "What is machine learning?"
5. Click "Send Message"

### Using the API

#### List Agents

```bash
curl http://localhost:8000/agents
```

#### Send a Message

```bash
curl -X POST http://localhost:8000/messages/send \
  -H "Content-Type: application/json" \
  -d '{
    "from_agent": "researcher_1",
    "to_agent": "analyst_1",
    "content": "Please analyze this data: Sales increased 20%",
    "message_type": "task"
  }'
```

#### Get Metrics

```bash
curl http://localhost:8000/metrics
```

### WebSocket Connection

Connect an agent via WebSocket:

```python
import asyncio
import websockets
import json

async def connect_agent():
    uri = "ws://localhost:8000/ws/researcher_1"
    async with websockets.connect(uri) as websocket:
        # Send a message
        message = {
            "id": "msg_1",
            "from_agent": "researcher_1",
            "to_agent": "analyst_1",
            "type": "text",
            "content": "Hello from WebSocket!"
        }
        await websocket.send(json.dumps(message))
        
        # Receive response
        response = await websocket.recv()
        print(json.loads(response))

asyncio.run(connect_agent())
```

## Python API Usage

### Create and Register an Agent

```python
from backend.agents.researcher_agent import ResearcherAgent
from backend.core.agent_manager import AgentManager
from backend.services.vector_service import VectorService

# Initialize services
vector_service = VectorService()
await vector_service.initialize()

# Create agent
researcher = ResearcherAgent(
    agent_id="my_researcher",
    name="My Researcher",
    vector_service=vector_service
)

# Register with manager
agent_manager = AgentManager()
await agent_manager.register_agent(
    researcher.agent_id,
    researcher.name,
    researcher.agent_type,
    researcher.get_capabilities()
)
```

### Send Messages Between Agents

```python
from backend.models.message import Message, MessageType

# Create message
message = Message(
    id="msg_1",
    from_agent="researcher_1",
    to_agent="analyst_1",
    type=MessageType.TASK,
    content="Analyze this data: ..."
)

# Send via agent manager
response = await agent_manager.send_message(
    from_agent="researcher_1",
    to_agent="analyst_1",
    content="Analyze this data: ...",
    message_type=MessageType.TASK
)
```

### Use Knowledge Base

```python
# Add knowledge
doc_id = await vector_service.add_knowledge(
    content="Python is a programming language.",
    metadata={"category": "programming"}
)

# Search knowledge
results = await vector_service.search(
    query="What is Python?",
    n_results=5
)
```

## Testing

Run the test suite:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest --cov=backend --cov-report=html tests/
```

## Troubleshooting

### Redis Connection Error

If you see Redis connection errors, the system will automatically fall back to in-memory queues. For production, ensure Redis is running.

### OpenAI API Errors

Make sure your `OPENAI_API_KEY` is set in the `.env` file and is valid.

### Port Already in Use

If port 8000 is in use, change it in `.env`:

```
SERVER_PORT=8001
```

### Vector Database Errors

If ChromaDB initialization fails, check that the `data/vectorstore` directory is writable.

## Next Steps

- Read the [Architecture Documentation](ARCHITECTURE.md)
- Explore the [API Documentation](README.md#api-endpoints)
- Check out example integrations in the `examples/` directory
- Customize agents for your use case

