"""
Smart Request Router - Routing Pattern Implementation

This module implements a routing system that intelligently directs user requests
to specialized handlers based on request analysis.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableBranch

load_dotenv()


class SmartRouter:
    """
    A smart router that analyzes requests and delegates them to appropriate handlers.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0,
        api_key: Optional[str] = None
    ):
        """Initialize the Smart Router."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self._build_router()
    
    def _build_router(self):
        """Build the routing chain with specialized handlers."""
        
        # Define specialized handlers
        def booking_handler(request: str) -> str:
            """Handles booking-related requests."""
            print("\n--- DELEGATING TO BOOKING HANDLER ---")
            # In a real application, this would integrate with booking APIs
            return f"Booking Handler: I'll help you with '{request}'. " \
                   f"Processing your booking request..."
        
        def info_handler(request: str) -> str:
            """Handles information requests."""
            print("\n--- DELEGATING TO INFO HANDLER ---")
            return f"Info Handler: I can help you with '{request}'. " \
                   f"Let me retrieve that information for you..."
        
        def support_handler(request: str) -> str:
            """Handles customer support requests."""
            print("\n--- DELEGATING TO SUPPORT HANDLER ---")
            return f"Support Handler: I understand you need help with '{request}'. " \
                   f"Let me assist you with that issue..."
        
        def unclear_handler(request: str) -> str:
            """Handles unclear or ambiguous requests."""
            print("\n--- HANDLING UNCLEAR REQUEST ---")
            return f"I'm not sure how to handle '{request}'. " \
                   f"Could you please clarify? Are you looking to:\n" \
                   f"- Book something (flights, hotels, restaurants)\n" \
                   f"- Get information about something\n" \
                   f"- Get customer support\n" \
                   f"- Something else?"
        
        # Router prompt - analyzes the request and decides which handler to use
        router_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a request routing coordinator. Analyze the user's request 
and determine which specialist handler should process it.

Routing rules:
- If the request is about booking, reservations, or scheduling (flights, hotels, restaurants, appointments), output 'booking'
- If the request is asking for information, facts, or explanations, output 'info'
- If the request is about problems, complaints, or needing help/support, output 'support'
- If the request is unclear or doesn't fit any category, output 'unclear'

ONLY output one word: 'booking', 'info', 'support', or 'unclear'."""),
            ("user", "{request}")
        ])
        
        router_chain = router_prompt | self.llm | StrOutputParser()
        
        # Define branches for each handler
        branches = {
            "booking": RunnablePassthrough.assign(
                output=lambda x: booking_handler(x['request']['request'])
            ),
            "info": RunnablePassthrough.assign(
                output=lambda x: info_handler(x['request']['request'])
            ),
            "support": RunnablePassthrough.assign(
                output=lambda x: support_handler(x['request']['request'])
            ),
            "unclear": RunnablePassthrough.assign(
                output=lambda x: unclear_handler(x['request']['request'])
            ),
        }
        
        # Create the routing branch
        delegation_branch = RunnableBranch(
            (lambda x: x['decision'].strip().lower() == 'booking', branches["booking"]),
            (lambda x: x['decision'].strip().lower() == 'info', branches["info"]),
            (lambda x: x['decision'].strip().lower() == 'support', branches["support"]),
            branches["unclear"]  # Default branch
        )
        
        # Combine router and delegation into final chain
        self.router_agent = {
            "decision": router_chain,
            "request": RunnablePassthrough()
        } | delegation_branch | (lambda x: x['output'])
    
    def route(self, request: str) -> str:
        """
        Route a request to the appropriate handler.
        
        Args:
            request: The user's request text
            
        Returns:
            The response from the appropriate handler
        """
        if not request or not request.strip():
            raise ValueError("Request cannot be empty")
        
        result = self.router_agent.invoke({"request": request})
        return result
    
    def route_with_decision(self, request: str) -> Dict[str, Any]:
        """
        Route a request and return both the decision and response.
        
        Args:
            request: The user's request text
            
        Returns:
            Dictionary with 'decision' and 'response' keys
        """
        if not request or not request.strip():
            raise ValueError("Request cannot be empty")
        
        # Get the routing decision
        router_prompt = ChatPromptTemplate.from_messages([
            ("system", """Analyze the request and output one word: 'booking', 'info', 'support', or 'unclear'."""),
            ("user", "{request}")
        ])
        decision_chain = router_prompt | self.llm | StrOutputParser()
        decision = decision_chain.invoke({"request": request}).strip().lower()
        
        # Get the response
        response = self.route(request)
        
        return {
            "decision": decision,
            "response": response,
            "request": request
        }


if __name__ == "__main__":
    router = SmartRouter()
    
    test_requests = [
        "Book me a flight to London",
        "What is the capital of France?",
        "I need help with my account",
        "Tell me about quantum physics",
        "Reserve a table for 4 people tonight",
        "My order hasn't arrived yet"
    ]
    
    print("=" * 70)
    print("SMART REQUEST ROUTER - ROUTING PATTERN DEMO")
    print("=" * 70)
    
    for req in test_requests:
        print(f"\nRequest: {req}")
        print("-" * 70)
        result = router.route_with_decision(req)
        print(f"Decision: {result['decision']}")
        print(f"Response: {result['response']}")

