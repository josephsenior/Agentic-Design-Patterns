"""
Safety Agent with Guardrails - Guardrails and Safety Patterns

This module implements safety guardrails to validate and filter agent outputs
for safety, appropriateness, and compliance.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class SafetyGuardrail:
    """
    A guardrail system that validates agent outputs for safety.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0,
        api_key: Optional[str] = None
    ):
        """Initialize the Safety Guardrail."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self._build_guardrail()
    
    def _build_guardrail(self):
        """Build the safety validation chain."""
        
        self.validation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a safety validator. Review the following content 
and determine if it's safe, appropriate, and compliant.

Check for:
- Harmful or dangerous content
- Inappropriate language
- Privacy violations
- Misinformation
- Bias or discrimination

Respond with:
- "SAFE" if the content is acceptable
- "UNSAFE" followed by the reason if it's not acceptable"""),
            ("user", "Content to validate: {content}")
        ])
        
        self.validation_chain = self.validation_prompt | self.llm | StrOutputParser()
    
    def validate(self, content: str) -> Dict[str, Any]:
        """
        Validate content for safety.
        
        Args:
            content: The content to validate
            
        Returns:
            Dictionary with validation result
        """
        if not content or not content.strip():
            return {
                "safe": False,
                "reason": "Empty content",
                "content": content
            }
        
        validation_result = self.validation_chain.invoke({"content": content})
        
        is_safe = "SAFE" in validation_result.upper()
        reason = validation_result if not is_safe else "Content is safe"
        
        return {
            "safe": is_safe,
            "reason": reason,
            "content": content,
            "validation_result": validation_result
        }
    
    def filter_unsafe(self, content: str) -> Dict[str, Any]:
        """
        Filter unsafe content and return safe alternative.
        
        Args:
            content: The content to filter
            
        Returns:
            Dictionary with filtered content or rejection
        """
        validation = self.validate(content)
        
        if validation["safe"]:
            return {
                "filtered": False,
                "original": content,
                "safe_content": content
            }
        
        # Generate safe alternative
        filter_prompt = ChatPromptTemplate.from_messages([
            ("system", """The following content was flagged as unsafe: {reason}
Generate a safe, appropriate alternative that maintains the intent but removes 
problematic elements."""),
            ("user", "Original content: {content}")
        ])
        
        filter_chain = filter_prompt | self.llm | StrOutputParser()
        safe_content = filter_chain.invoke({
            "content": content,
            "reason": validation["reason"]
        })
        
        return {
            "filtered": True,
            "original": content,
            "safe_content": safe_content,
            "reason": validation["reason"]
        }


class GuardedAgent:
    """
    An agent with built-in safety guardrails.
    """
    
    def __init__(self, llm, guardrail: SafetyGuardrail):
        self.llm = llm
        self.guardrail = guardrail
    
    def generate_safe(self, prompt: str) -> Dict[str, Any]:
        """
        Generate content with safety validation.
        
        Args:
            prompt: The generation prompt
            
        Returns:
            Dictionary with generated content and safety status
        """
        # Generate content
        generation_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("user", "{prompt}")
        ])
        generation_chain = generation_prompt | self.llm | StrOutputParser()
        generated = generation_chain.invoke({"prompt": prompt})
        
        # Validate
        validation = self.guardrail.validate(generated)
        
        if not validation["safe"]:
            # Try to filter
            filtered = self.guardrail.filter_unsafe(generated)
            return {
                "original": generated,
                "safe_content": filtered["safe_content"],
                "was_filtered": True,
                "validation": validation
            }
        
        return {
            "original": generated,
            "safe_content": generated,
            "was_filtered": False,
            "validation": validation
        }


if __name__ == "__main__":
    from langchain_openai import ChatOpenAI
    
    guardrail = SafetyGuardrail()
    llm = ChatOpenAI()
    agent = GuardedAgent(llm, guardrail)
    
    print("=" * 70)
    print("SAFETY GUARDRAILS - GUARDRAILS AND SAFETY PATTERNS")
    print("=" * 70)
    
    # Test validation
    test_contents = [
        "The weather is nice today.",
        "Here's how to create a helpful response."
    ]
    
    for content in test_contents:
        print(f"\n📝 Validating: {content[:50]}...")
        result = guardrail.validate(content)
        print(f"✅ Safe: {result['safe']}")
        if not result['safe']:
            print(f"⚠️  Reason: {result['reason']}")

