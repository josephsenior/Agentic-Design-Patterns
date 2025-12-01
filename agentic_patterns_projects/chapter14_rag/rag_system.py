"""
RAG System - Knowledge Retrieval Pattern (RAG)

This module implements a Retrieval-Augmented Generation (RAG) system that
combines document retrieval with LLM generation for accurate, context-aware responses.
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema.runnable import RunnablePassthrough

load_dotenv()


class RAGSystem:
    """
    A Retrieval-Augmented Generation system for question answering.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0,
        api_key: Optional[str] = None
    ):
        """Initialize the RAG System."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self.embeddings = OpenAIEmbeddings(api_key=api_key)
        self.vectorstore = None
        self.retriever = None
        self._build_rag_chain()
    
    def _build_rag_chain(self):
        """Build the RAG chain."""
        # RAG prompt template
        self.rag_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant that answers questions based on 
the provided context. Use only the information from the context to answer questions. 
If the context doesn't contain enough information to answer the question, say so.

Context:
{context}

Answer the question based on the context above."""),
            ("user", "{question}")
        ])
        
        # RAG chain will be built after documents are loaded
        self.rag_chain = None
    
    def load_documents(self, documents: List[str], chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Load and process documents for retrieval.
        
        Args:
            documents: List of document texts
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        # Convert to Document objects
        doc_objects = [Document(page_content=doc) for doc in documents]
        
        # Split documents into chunks
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator="\n"
        )
        chunks = text_splitter.split_documents(doc_objects)
        
        # Create vector store
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        
        # Build RAG chain
        self.rag_chain = (
            {
                "context": self.retriever | self._format_docs,
                "question": RunnablePassthrough()
            }
            | self.rag_prompt
            | self.llm
            | StrOutputParser()
        )
        
        print(f"Loaded {len(chunks)} document chunks into vector store")
    
    def _format_docs(self, docs: List[Document]) -> str:
        """Format documents for the prompt."""
        return "\n\n".join([doc.page_content for doc in docs])
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Query the RAG system.
        
        Args:
            question: The question to answer
            
        Returns:
            Dictionary with answer and retrieved context
        """
        if not self.rag_chain:
            raise ValueError("Documents must be loaded first. Call load_documents()")
        
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        
        # Retrieve relevant documents
        retrieved_docs = self.retriever.invoke(question)
        
        # Generate answer
        answer = self.rag_chain.invoke(question)
        
        return {
            "question": question,
            "answer": answer,
            "retrieved_documents": [doc.page_content for doc in retrieved_docs],
            "num_retrieved": len(retrieved_docs)
        }
    
    def add_documents(self, documents: List[str]):
        """
        Add more documents to the existing knowledge base.
        
        Args:
            documents: List of new document texts
        """
        if not self.vectorstore:
            self.load_documents(documents)
            return
        
        # Convert to Document objects and split
        doc_objects = [Document(page_content=doc) for doc in documents]
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separator="\n"
        )
        chunks = text_splitter.split_documents(doc_objects)
        
        # Add to existing vector store
        self.vectorstore.add_documents(chunks)
        print(f"Added {len(chunks)} new document chunks")


if __name__ == "__main__":
    # Sample knowledge base
    knowledge_base = [
        """
        Artificial Intelligence (AI) is a branch of computer science that aims to create 
        intelligent machines capable of performing tasks that typically require human intelligence. 
        These tasks include learning, reasoning, problem-solving, perception, and language understanding.
        """,
        """
        Machine Learning is a subset of AI that enables systems to learn and improve from 
        experience without being explicitly programmed. It uses algorithms to analyze data, 
        identify patterns, and make decisions or predictions.
        """,
        """
        Deep Learning is a subset of machine learning that uses neural networks with multiple 
        layers (hence "deep") to model and understand complex patterns. It has been particularly 
        successful in image recognition, natural language processing, and speech recognition.
        """,
        """
        Natural Language Processing (NLP) is a field of AI that focuses on the interaction 
        between computers and human language. It enables machines to read, understand, and 
        generate human language in a valuable way.
        """,
        """
        Large Language Models (LLMs) are AI systems trained on vast amounts of text data. 
        They can generate human-like text, answer questions, translate languages, and perform 
        various language tasks. Examples include GPT-4, Claude, and Gemini.
        """
    ]
    
    rag = RAGSystem()
    
    print("=" * 70)
    print("RAG SYSTEM - KNOWLEDGE RETRIEVAL PATTERN")
    print("=" * 70)
    
    print("\nLoading knowledge base...")
    rag.load_documents(knowledge_base)
    
    questions = [
        "What is Artificial Intelligence?",
        "How does machine learning differ from deep learning?",
        "What are Large Language Models?",
        "What is Natural Language Processing used for?"
    ]
    
    for question in questions:
        print("\n" + "=" * 70)
        print(f"Question: {question}")
        print("=" * 70)
        result = rag.query(question)
        print(f"\nAnswer: {result['answer']}")
        print(f"\nRetrieved {result['num_retrieved']} relevant documents")

