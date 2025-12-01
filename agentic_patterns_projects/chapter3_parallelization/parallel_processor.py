"""
Parallel Document Processor - Parallelization Pattern Implementation

This module demonstrates parallel processing of independent tasks using
LangChain's RunnableParallel to execute multiple operations concurrently.
"""

import os
import asyncio
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

load_dotenv()


class ParallelProcessor:
    """
    A processor that executes multiple independent analysis tasks in parallel.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        """Initialize the Parallel Processor."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self._build_chains()
    
    def _build_chains(self):
        """Build parallel processing chains."""
        
        # Chain 1: Summarize the document
        self.summarize_chain = (
            ChatPromptTemplate.from_messages([
                ("system", "Summarize the following document concisely, highlighting the main points:"),
                ("user", "{document}")
            ])
            | self.llm
            | StrOutputParser()
        )
        
        # Chain 2: Extract key entities
        self.entities_chain = (
            ChatPromptTemplate.from_messages([
                ("system", "Extract and list all important entities (people, organizations, locations, dates) from the document:"),
                ("user", "{document}")
            ])
            | self.llm
            | StrOutputParser()
        )
        
        # Chain 3: Identify main topics
        self.topics_chain = (
            ChatPromptTemplate.from_messages([
                ("system", "Identify the main topics and themes in the document:"),
                ("user", "{document}")
            ])
            | self.llm
            | StrOutputParser()
        )
        
        # Chain 4: Generate questions
        self.questions_chain = (
            ChatPromptTemplate.from_messages([
                ("system", "Generate 3-5 thought-provoking questions based on the document:"),
                ("user", "{document}")
            ])
            | self.llm
            | StrOutputParser()
        )
        
        # Chain 5: Extract key terms
        self.terms_chain = (
            ChatPromptTemplate.from_messages([
                ("system", "List 5-10 key terms or concepts from the document, separated by commas:"),
                ("user", "{document}")
            ])
            | self.llm
            | StrOutputParser()
        )
        
        # Parallel execution of all chains
        self.parallel_chain = RunnableParallel({
            "summary": self.summarize_chain,
            "entities": self.entities_chain,
            "topics": self.topics_chain,
            "questions": self.questions_chain,
            "key_terms": self.terms_chain,
            "document": RunnablePassthrough()  # Keep original document
        })
        
        # Synthesis chain that combines all parallel results
        self.synthesis_prompt = ChatPromptTemplate.from_messages([
            ("system", """Based on the following parallel analysis results, create a comprehensive report:

Summary: {summary}
Entities: {entities}
Topics: {topics}
Questions: {questions}
Key Terms: {key_terms}

Create a well-structured report that synthesizes all this information."""),
            ("user", "Original Document: {document}")
        ])
        
        # Full chain: parallel processing + synthesis
        self.full_chain = (
            self.parallel_chain
            | self.synthesis_prompt
            | self.llm
            | StrOutputParser()
        )
    
    async def process_async(self, document: str) -> Dict[str, Any]:
        """
        Process a document asynchronously with parallel analysis.
        
        Args:
            document: The document text to process
            
        Returns:
            Dictionary with all analysis results
        """
        if not document or not document.strip():
            raise ValueError("Document cannot be empty")
        
        # Execute parallel analysis
        parallel_results = await self.parallel_chain.ainvoke({"document": document})
        
        # Execute synthesis
        synthesis = await self.full_chain.ainvoke({"document": document})
        
        return {
            "parallel_results": parallel_results,
            "synthesis": synthesis
        }
    
    def process(self, document: str) -> Dict[str, Any]:
        """
        Process a document synchronously.
        
        Args:
            document: The document text to process
            
        Returns:
            Dictionary with all analysis results
        """
        if not document or not document.strip():
            raise ValueError("Document cannot be empty")
        
        # Execute parallel analysis
        parallel_results = self.parallel_chain.invoke({"document": document})
        
        # Execute synthesis
        synthesis = self.full_chain.invoke({"document": document})
        
        return {
            "parallel_results": parallel_results,
            "synthesis": synthesis
        }
    
    async def process_batch_async(self, documents: List[str]) -> List[Dict[str, Any]]:
        """
        Process multiple documents in parallel.
        
        Args:
            documents: List of document texts
            
        Returns:
            List of analysis results for each document
        """
        tasks = [self.process_async(doc) for doc in documents]
        results = await asyncio.gather(*tasks)
        return results


if __name__ == "__main__":
    sample_document = """
    Artificial Intelligence has revolutionized many industries in recent years. 
    Machine learning algorithms, particularly deep learning, have enabled breakthroughs 
    in computer vision, natural language processing, and robotics. Companies like 
    OpenAI, Google, and Microsoft are leading the research in this field. 
    The development of large language models such as GPT-4 has opened new possibilities 
    for AI applications. However, concerns about AI safety, ethics, and job displacement 
    continue to be important topics of discussion.
    """
    
    processor = ParallelProcessor()
    
    print("=" * 70)
    print("PARALLEL DOCUMENT PROCESSOR - PARALLELIZATION PATTERN")
    print("=" * 70)
    
    print("\n📄 Processing document with parallel analysis...")
    result = processor.process(sample_document)
    
    print("\n" + "=" * 70)
    print("PARALLEL RESULTS")
    print("=" * 70)
    for key, value in result["parallel_results"].items():
        if key != "document":
            print(f"\n{key.upper()}:")
            print(f"  {value}")
    
    print("\n" + "=" * 70)
    print("SYNTHESIS")
    print("=" * 70)
    print(result["synthesis"])

