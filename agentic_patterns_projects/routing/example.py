"""
Example usage of the Smart Router
"""

from smart_router import SmartRouter


def example_basic_routing():
    """Basic routing examples."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Request Routing")
    print("=" * 70)
    
    router = SmartRouter()
    
    requests = [
        "I want to book a hotel room in Paris",
        "What's the weather like today?",
        "I'm having trouble logging into my account",
        "Can you tell me about machine learning?"
    ]
    
    for req in requests:
        print(f"\nRequest: {req}")
        result = router.route_with_decision(req)
        print(f"   Routed to: {result['decision']}")
        print(f"   Response: {result['response']}")


def example_customer_support_scenario():
    """Simulate a customer support scenario."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Customer Support Scenario")
    print("=" * 70)
    
    router = SmartRouter()
    
    customer_requests = [
        "Book a flight from New York to Tokyo",
        "What are your business hours?",
        "My package was damaged during shipping",
        "Reserve a table for dinner",
        "How do I return an item?",
        "What's the return policy?"
    ]
    
    print("\nCustomer Support Center - Request Routing\n")
    for i, req in enumerate(customer_requests, 1):
        print(f"\n[{i}] Customer: {req}")
        result = router.route_with_decision(req)
        print(f"    System: Routing to {result['decision']} handler...")
        print(f"    {result['response']}")


if __name__ == "__main__":
    example_basic_routing()
    example_customer_support_scenario()

