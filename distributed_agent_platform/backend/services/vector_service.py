import os
from typing import List, Optional, Dict, Any
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()


class VectorService:
    """ChromaDB-based vector service for knowledge storage and retrieval."""
    
    def __init__(self, persist_dir: Optional[str] = None):
        self.persist_dir = persist_dir or os.getenv(
            "CHROMA_PERSIST_DIR",
            "./data/vectorstore"
        )
        self.client: Optional[chromadb.Client] = None
        self.collection: Optional[chromadb.Collection] = None
        self.embedder: Optional[SentenceTransformer] = None
    
    async def initialize(self, collection_name: str = "agent_knowledge"):
        """Initialize the vector service."""
        try:
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "Agent knowledge base"}
            )
            
            # Initialize embedding model
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            
        except Exception as e:
            print(f"Failed to initialize vector service: {e}")
            self.client = None
            self.collection = None
    
    async def add_knowledge(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        doc_id: Optional[str] = None
    ) -> str:
        """Add knowledge to the vector store."""
        if not self.collection or not self.embedder:
            raise RuntimeError("Vector service not initialized")
        
        # Generate embedding
        embedding = self.embedder.encode(content).tolist()
        
        # Prepare metadata
        doc_metadata = metadata or {}
        doc_metadata["content"] = content
        
        # Add to collection
        if doc_id is None:
            import uuid
            doc_id = str(uuid.uuid4())
        
        self.collection.add(
            embeddings=[embedding],
            documents=[content],
            metadatas=[doc_metadata],
            ids=[doc_id]
        )
        
        return doc_id
    
    async def search(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search the knowledge base."""
        if not self.collection or not self.embedder:
            return []
        
        # Generate query embedding
        query_embedding = self.embedder.encode(query).tolist()
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_metadata
        )
        
        # Format results
        formatted_results = []
        if results["documents"] and results["documents"][0]:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None
                })
        
        return formatted_results
    
    async def delete_knowledge(self, doc_id: str) -> bool:
        """Delete knowledge from the vector store."""
        if not self.collection:
            return False
        
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except:
            return False
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        if not self.collection:
            return {"count": 0}
        
        count = self.collection.count()
        return {
            "count": count,
            "name": self.collection.name
        }

