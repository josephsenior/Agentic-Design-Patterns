# Agentic Design Patterns - Complete Real-World Projects

This directory contains complete, production-ready implementations of all 21 design patterns from the Agentic Design Patterns book. Each project demonstrates a specific pattern with a practical, runnable application.

## All 21 Patterns Implemented

### Core Patterns (Chapters 1-8)

1. **Chapter 1: Prompt Chaining** - `chapter1_prompt_chaining/`
   - **Project**: Document Analysis Pipeline
   - **Pattern**: Sequential multi-step processing
   - **Use Case**: Extract → Entities → Summary → JSON

2. **Chapter 2: Routing** - `chapter2_routing/`
   - **Project**: Smart Request Router
   - **Pattern**: Request classification and delegation
   - **Use Case**: Route requests to specialized handlers

3. **Chapter 3: Parallelization** - `chapter3_parallelization/`
   - **Project**: Parallel Document Processor
   - **Pattern**: Concurrent task execution
   - **Use Case**: 5 parallel analysis tasks with synthesis

4. **Chapter 4: Reflection** - `chapter4_reflection/`
   - **Project**: Self-Improving Content Generator
   - **Pattern**: Generate → Critique → Refine
   - **Use Case**: Iterative content improvement

5. **Chapter 5: Tool Use** - `chapter5_tool_use/`
   - **Project**: Research Assistant with Tools
   - **Pattern**: Function calling and tool integration
   - **Use Case**: Search, calculate, analyze with tools

6. **Chapter 6: Planning** - `chapter6_planning/`
   - **Project**: Task Planning System
   - **Pattern**: Goal decomposition and execution
   - **Use Case**: Break goals into actionable tasks

7. **Chapter 7: Multi-Agent** - `chapter7_multi_agent/`
   - **Project**: Collaborative Team System
   - **Pattern**: Multiple specialized agents working together
   - **Use Case**: Research → Write → Edit → Coordinate

8. **Chapter 8: Memory** - `chapter8_memory/`
   - **Project**: Conversation Memory System
   - **Pattern**: State persistence and context management
   - **Use Case**: Maintain conversation history

### Advanced Patterns (Chapters 9-14)

9. **Chapter 9: Adaptation** - `chapter9_adaptation/`
   - **Project**: Adaptive Agent
   - **Pattern**: Learning from feedback
   - **Use Case**: Improve over time based on experience

10. **Chapter 10: MCP** - `chapter10_mcp/`
    - **Project**: Model Context Protocol Integration
    - **Pattern**: Standardized agent communication
    - **Use Case**: Tool sharing and resource access

11. **Chapter 11: Goal Setting** - `chapter11_goal_setting/`
    - **Project**: Goal-Oriented Agent
    - **Pattern**: Goal breakdown and progress tracking
    - **Use Case**: Set goals, track progress, achieve objectives

12. **Chapter 12: Exception Handling** - `chapter12_exception_handling/`
    - **Project**: Robust Agent with Fallback
    - **Pattern**: Error handling and recovery
    - **Use Case**: Graceful failure handling

13. **Chapter 13: Human-in-the-Loop** - `chapter13_human_in_loop/`
    - **Project**: Interactive Agent
    - **Pattern**: Human escalation and feedback
    - **Use Case**: Customer support with escalation

14. **Chapter 14: RAG** - `chapter14_rag/`
    - **Project**: Knowledge Retrieval System
    - **Pattern**: Retrieval-Augmented Generation
    - **Use Case**: Document-based Q&A

### Specialized Patterns (Chapters 15-21)

15. **Chapter 15: Inter-Agent Communication** - `chapter15_inter_agent/`
    - **Project**: Agent Communication System
    - **Pattern**: Agent-to-agent messaging
    - **Use Case**: Agents collaborating via messages

16. **Chapter 16: Resource Optimization** - `chapter16_resource_optimization/`
    - **Project**: Resource Optimizer
    - **Pattern**: Efficient resource usage
    - **Use Case**: Caching, batching, cost optimization

17. **Chapter 17: Reasoning** - `chapter17_reasoning/`
    - **Project**: Chain-of-Thought Agent
    - **Pattern**: Step-by-step reasoning
    - **Use Case**: Complex problem solving

18. **Chapter 18: Guardrails** - `chapter18_guardrails/`
    - **Project**: Safety Agent
    - **Pattern**: Content validation and filtering
    - **Use Case**: Safety and compliance checking

19. **Chapter 19: Evaluation** - `chapter19_evaluation/`
    - **Project**: Agent Evaluation System
    - **Pattern**: LLM-as-a-Judge
    - **Use Case**: Quality assessment and monitoring

20. **Chapter 20: Prioritization** - `chapter20_prioritization/`
    - **Project**: Task Prioritization System
    - **Pattern**: Priority-based task management
    - **Use Case**: Rank and order tasks

21. **Chapter 21: Exploration** - `chapter21_exploration/`
    - **Project**: Exploration Agent
    - **Pattern**: Experimental discovery
    - **Use Case**: Multiple approach testing

## Quick Start

Getting started with any project is straightforward:

```bash
# 1. Navigate to the project you want to explore
cd agentic_patterns_projects/chapterX_pattern/

# 2. Install the dependencies
pip install -r requirements.txt

# 3. Set up your environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 4. Run the example
python main_file.py
```

## Project Structure

Each project follows a consistent structure that makes it easy to understand and extend:

```
chapterX_pattern/
├── main_file.py          # Core implementation
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
└── .env.example         # Environment template
```

## Pattern Categories

I've organized the patterns into categories to help you understand how they relate:

**Sequential Patterns**
- Prompt Chaining, Planning

**Parallel Patterns**
- Parallelization

**Decision Patterns**
- Routing, Reflection, Prioritization

**Integration Patterns**
- Tool Use, Multi-Agent, Inter-Agent Communication, MCP

**State Patterns**
- Memory Management, Goal Setting

**Quality Patterns**
- Exception Handling, Guardrails, Evaluation

**Advanced Patterns**
- Adaptation, RAG, Reasoning, Human-in-the-Loop, Resource Optimization, Exploration

## Common Requirements

Most projects share similar requirements:

- Python 3.8 or higher
- OpenAI API key (you'll set this in your `.env` file)
- LangChain libraries (installed via requirements.txt)

## Installation

To get started, install the common dependencies:

```bash
# Install common dependencies
pip install langchain langchain-openai langchain-community python-dotenv

# For specific projects, check their requirements.txt for any additional packages
```

## Usage Examples

Here are some quick examples to get you started:

### Example 1: Prompt Chaining
```python
from document_analyzer import DocumentAnalyzer
analyzer = DocumentAnalyzer()
result = analyzer.analyze("Your document text...")
```

### Example 2: Routing
```python
from smart_router import SmartRouter
router = SmartRouter()
result = router.route("Book me a flight")
```

### Example 3: Multi-Agent
```python
from collaborative_team import CollaborativeTeam
team = CollaborativeTeam()
result = team.collaborate("Create a blog post", "Requirements...")
```

## Learning Path

If you're new to agentic design patterns, here's a suggested learning path:

1. **Start with Core Patterns** (Chapters 1-8)
   - These cover the fundamentals
   - You'll learn how to build sequential and parallel workflows
   - Great foundation for everything else

2. **Explore Advanced Patterns** (Chapters 9-14)
   - Learn about adaptation and memory systems
   - Implement RAG and human interaction patterns
   - These build on the core concepts

3. **Master Specialized Patterns** (Chapters 15-21)
   - Dive into resource optimization
   - Implement safety and evaluation systems
   - These are the advanced techniques you'll use in production

## Documentation

Each project includes comprehensive documentation:

- Complete implementation with comments
- README explaining the pattern and how it works
- Usage examples you can run right away
- Architecture diagrams (in the README)
- Proper error handling
- Type hints for better code clarity

## Integration

One of the coolest things about these patterns is that you can combine them:

- Use **Routing** with **Multi-Agent** for complex workflows
- Combine **RAG** with **Tool Use** for enhanced capabilities
- Add **Guardrails** to any agent for safety
- Use **Evaluation** to monitor all agents

Feel free to experiment and mix patterns to solve your specific problems.

## Status

**All 21 patterns are complete and ready to use**

Every pattern has been implemented as a production-ready project. You can use these as building blocks for your own agentic systems or learn from them to understand how different patterns work.

## Contributing

Each project is self-contained and can be extended independently. If you want to contribute:

- Add more examples
- Integrate with your own systems
- Combine patterns in new ways
- Extend functionality

These are educational examples, so feel free to experiment and build on them.

## License

These projects are educational examples demonstrating agentic design patterns. Use them to learn, experiment, and build your own systems.

---

Happy building! If you have questions or want to discuss these patterns, feel free to open an issue or start a discussion.
