"""
Conversation Memory System - Memory Management Pattern

This module implements memory management for maintaining conversation context
and state across multiple interactions.
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.chains import ConversationChain

load_dotenv()


class ConversationMemory:
    """
    A conversation system with memory management.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        memory_type: str = "buffer",  # "buffer" or "summary"
        api_key: Optional[str] = None
    ):
        """
        Initialize the Conversation Memory system.
        
        Args:
            model_name: The OpenAI model to use
            temperature: Sampling temperature
            memory_type: Type of memory ("buffer" or "summary")
            api_key: OpenAI API key
        """
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self.memory_type = memory_type
        self._initialize_memory()
        self._build_chain()
    
    def _initialize_memory(self):
        """Initialize the memory system."""
        if self.memory_type == "buffer":
            self.memory = ConversationBufferMemory(
                return_messages=True,
                memory_key="history"
            )
        elif self.memory_type == "summary":
            self.memory = ConversationSummaryMemory(
                llm=self.llm,
                return_messages=True,
                memory_key="history"
            )
        else:
            raise ValueError(f"Unknown memory type: {self.memory_type}")
    
    def _build_chain(self):
        """Build the conversation chain with memory."""
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a helpful assistant with memory of our conversation. 
You remember previous interactions and can reference them in your responses."""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        self.chain = ConversationChain(
            llm=self.llm,
            prompt=prompt,
            memory=self.memory,
            verbose=False
        )
    
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Send a message and get a response with memory.
        
        Args:
            message: The user's message
            
        Returns:
            Dictionary with response and conversation state
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")
        
        response = self.chain.predict(input=message)
        
        return {
            "user_message": message,
            "assistant_response": response,
            "memory_type": self.memory_type,
            "conversation_length": len(self.memory.chat_memory.messages)
        }
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the full conversation history.
        
        Returns:
            List of message dictionaries
        """
        messages = []
        for msg in self.memory.chat_memory.messages:
            if isinstance(msg, HumanMessage):
                messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                messages.append({"role": "assistant", "content": msg.content})
        
        return messages
    
    def clear_memory(self):
        """Clear the conversation memory."""
        self.memory.clear()
        print("🧹 Memory cleared")
    
    def get_memory_summary(self) -> str:
        """
        Get a summary of the conversation (for summary memory type).
        
        Returns:
            Memory summary string
        """
        if self.memory_type == "summary":
            return self.memory.moving_summary_buffer
        else:
            # For buffer memory, return a count
            return f"Buffer memory with {len(self.memory.chat_memory.messages)} messages"


class ContextualAgent:
    """
    An agent that maintains context across multiple interactions.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        """Initialize the Contextual Agent."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        # Manual context management
        self.conversation_context = []
        self.user_preferences = {}
        self.facts_learned = []
    
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Chat with context awareness.
        
        Args:
            message: User's message
            
        Returns:
            Response with context
        """
        # Build context-aware prompt
        context_str = "\n".join([
            f"User: {ctx['user']}\nAssistant: {ctx['assistant']}"
            for ctx in self.conversation_context[-5:]  # Last 5 exchanges
        ])
        
        preferences_str = "\n".join([
            f"- {key}: {value}"
            for key, value in self.user_preferences.items()
        ]) if self.user_preferences else "None"
        
        facts_str = "\n".join([f"- {fact}" for fact in self.facts_learned[-5:]])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are a helpful assistant that remembers context.

Recent Conversation:
{context_str if context_str else "No previous conversation"}

User Preferences:
{preferences_str}

Facts Learned:
{facts_str if facts_str else "None"}

Use this context to provide relevant, personalized responses."""),
            ("user", "{message}")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        response = chain.invoke({"message": message})
        
        # Update context
        self.conversation_context.append({
            "user": message,
            "assistant": response
        })
        
        # Extract and store preferences/facts (simplified)
        if "my name is" in message.lower():
            name = message.split("my name is")[-1].strip().split()[0]
            self.user_preferences["name"] = name
        
        return {
            "user_message": message,
            "assistant_response": response,
            "context_length": len(self.conversation_context)
        }
    
    def get_context(self) -> Dict[str, Any]:
        """Get current context state."""
        return {
            "conversation_history": self.conversation_context,
            "user_preferences": self.user_preferences,
            "facts_learned": self.facts_learned
        }
    
    def clear_context(self):
        """Clear all context."""
        self.conversation_context = []
        self.user_preferences = {}
        self.facts_learned = []
        print("🧹 Context cleared")


if __name__ == "__main__":
    print("=" * 70)
    print("CONVERSATION MEMORY SYSTEM - MEMORY MANAGEMENT PATTERN")
    print("=" * 70)
    
    # Example 1: Buffer Memory
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Buffer Memory")
    print("=" * 70)
    
    memory_system = ConversationMemory(memory_type="buffer")
    
    messages = [
        "My name is Alice",
        "What's my name?",
        "I like programming in Python",
        "What programming language do I like?",
        "What's my name again?"
    ]
    
    for msg in messages:
        print(f"\n👤 User: {msg}")
        result = memory_system.chat(msg)
        print(f"🤖 Assistant: {result['assistant_response']}")
    
    print(f"\n📊 Conversation History ({len(memory_system.get_conversation_history())} messages)")
    
    # Example 2: Contextual Agent
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Contextual Agent")
    print("=" * 70)
    
    contextual_agent = ContextualAgent()
    
    for msg in messages:
        print(f"\n👤 User: {msg}")
        result = contextual_agent.chat(msg)
        print(f"🤖 Assistant: {result['assistant_response']}")
    
    print(f"\n📊 Context: {contextual_agent.get_context()}")

