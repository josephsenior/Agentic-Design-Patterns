"""
Document Analysis Pipeline using Prompt Chaining Pattern

This module implements a multi-step document analysis pipeline that demonstrates
the prompt chaining pattern from Agentic Design Patterns.

The pipeline consists of:
1. Information Extraction
2. Entity Identification
3. Summary Generation
4. Structured Output Formatting
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.json import SimpleJsonOutputParser
import json

# Load environment variables
load_dotenv()


class DocumentAnalyzer:
    """
    A document analysis system using prompt chaining to process documents
    through multiple sequential steps.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0,
        api_key: Optional[str] = None
    ):
        """
        Initialize the Document Analyzer.
        
        Args:
            model_name: The OpenAI model to use
            temperature: Sampling temperature (0 for deterministic output)
            api_key: OpenAI API key (if not provided, uses OPENAI_API_KEY env var)
        """
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        # Initialize the prompt chain
        self._build_chain()
    
    def _build_chain(self):
        """
        Build the prompt chaining pipeline using LangChain's LCEL.
        
        This creates a sequential chain where each step's output becomes
        the next step's input.
        """
        
        # Step 1: Extract key information from the document
        self.prompt_extract = ChatPromptTemplate.from_template(
            """You are an expert document analyst. Extract the key information from the following document.

Focus on:
- Main topics and themes
- Key facts and figures
- Important dates and events
- Notable claims or statements

Document:
{document}

Extract the key information in a clear, structured format."""
        )
        
        # Step 2: Identify entities (people, organizations, locations, etc.)
        self.prompt_entities = ChatPromptTemplate.from_template(
            """You are an entity extraction specialist. Based on the following extracted information, 
identify and list all important entities.

Extracted Information:
{extracted_info}

Identify and list:
- People (names, titles, roles)
- Organizations (companies, institutions, groups)
- Locations (cities, countries, places)
- Dates and time periods
- Key concepts or topics

Format your response as a structured list."""
        )
        
        # Step 3: Generate a concise summary
        self.prompt_summary = ChatPromptTemplate.from_template(
            """You are a professional summarizer. Create a concise, informative summary 
based on the extracted information and identified entities.

Extracted Information:
{extracted_info}

Identified Entities:
{entities}

Create a 2-3 sentence summary that captures the essence of the document."""
        )
        
        # Step 4: Structure everything into JSON format
        self.prompt_structure = ChatPromptTemplate.from_template(
            """You are a data structuring specialist. Transform the following information 
into a well-structured JSON object.

Extracted Information:
{extracted_info}

Identified Entities:
{entities}

Summary:
{summary}

Create a JSON object with the following structure:
{{
    "summary": "<the summary text>",
    "entities": {{
        "people": ["list of people"],
        "organizations": ["list of organizations"],
        "locations": ["list of locations"],
        "dates": ["list of dates"],
        "concepts": ["list of key concepts"]
    }},
    "key_facts": ["list of important facts"],
    "main_topics": ["list of main topics"]
}}

Return ONLY valid JSON, no additional text."""
        )
        
        # Build the chain using LangChain Expression Language (LCEL)
        # Step 1: Extract information
        extraction_chain = (
            self.prompt_extract 
            | self.llm 
            | StrOutputParser()
        )
        
        # Step 2: Identify entities (uses output from step 1)
        entity_chain = (
            {"extracted_info": extraction_chain}
            | self.prompt_entities
            | self.llm
            | StrOutputParser()
        )
        
        # Step 3: Generate summary (uses outputs from steps 1 and 2)
        summary_chain = (
            {
                "extracted_info": extraction_chain,
                "entities": entity_chain
            }
            | self.prompt_summary
            | self.llm
            | StrOutputParser()
        )
        
        # Step 4: Structure into JSON (uses all previous outputs)
        self.full_chain = (
            {
                "extracted_info": extraction_chain,
                "entities": entity_chain,
                "summary": summary_chain
            }
            | self.prompt_structure
            | self.llm
            | StrOutputParser()
        )
    
    def analyze(self, document: str) -> Dict[str, Any]:
        """
        Analyze a document through the complete prompt chaining pipeline.
        
        Args:
            document: The text content of the document to analyze
            
        Returns:
            A dictionary containing the structured analysis results
        """
        if not document or not document.strip():
            raise ValueError("Document text cannot be empty")
        
        # Execute the full chain
        result = self.full_chain.invoke({"document": document})
        
        # Parse JSON output
        try:
            # Try to extract JSON from the response (in case there's extra text)
            json_start = result.find('{')
            json_end = result.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = result[json_start:json_end]
                return json.loads(json_str)
            else:
                return json.loads(result)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return the raw result with error info
            return {
                "error": "Failed to parse JSON output",
                "raw_output": result,
                "parse_error": str(e)
            }
    
    def analyze_step_by_step(self, document: str) -> Dict[str, Any]:
        """
        Analyze a document and return intermediate results from each step.
        Useful for debugging and understanding the pipeline.
        
        Args:
            document: The text content of the document to analyze
            
        Returns:
            A dictionary containing results from each step
        """
        if not document or not document.strip():
            raise ValueError("Document text cannot be empty")
        
        # Execute each step individually to capture intermediate results
        step1_result = (self.prompt_extract | self.llm | StrOutputParser()).invoke(
            {"document": document}
        )
        
        step2_result = (self.prompt_entities | self.llm | StrOutputParser()).invoke(
            {"extracted_info": step1_result}
        )
        
        step3_result = (self.prompt_summary | self.llm | StrOutputParser()).invoke(
            {
                "extracted_info": step1_result,
                "entities": step2_result
            }
        )
        
        step4_result = (self.prompt_structure | self.llm | StrOutputParser()).invoke(
            {
                "extracted_info": step1_result,
                "entities": step2_result,
                "summary": step3_result
            }
        )
        
        return {
            "step1_extraction": step1_result,
            "step2_entities": step2_result,
            "step3_summary": step3_result,
            "step4_structured": step4_result,
            "final_json": self._parse_json(step4_result)
        }
    
    def _parse_json(self, text: str) -> Dict[str, Any]:
        """Helper method to parse JSON from text."""
        try:
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = text[json_start:json_end]
                return json.loads(json_str)
            return json.loads(text)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw": text}


if __name__ == "__main__":
    # Example usage
    sample_document = """
    TechCorp Inc. announced today that CEO Sarah Johnson will be stepping down 
    after 15 years of leadership. The company, based in San Francisco, reported 
    record quarterly earnings of $2.5 billion. Johnson will be succeeded by 
    former COO Michael Chen, effective January 15, 2024. The transition comes 
    as TechCorp expands into artificial intelligence and cloud computing markets.
    """
    
    analyzer = DocumentAnalyzer()
    result = analyzer.analyze(sample_document)
    
    print("=" * 60)
    print("DOCUMENT ANALYSIS RESULTS")
    print("=" * 60)
    print(json.dumps(result, indent=2))
    print("=" * 60)

