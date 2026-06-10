"""
Vector Store Memory using ChromaDB
"""
from typing import List, Dict, Any, Optional
import chromadb
from config import settings
from utils.logger import logger

class VectorStoreMemory:
    """Vector store for semantic memory"""
    
    def __init__(self):
        # Initialize ChromaDB with new client API
        try:
            self.client = chromadb.PersistentClient(
                path=str(settings.chroma_db_path)
            )
        except Exception as e:
            logger.warning(f"Failed to create persistent client, using ephemeral: {e}")
            self.client = chromadb.EphemeralClient()
        
        self.collection = self.client.get_or_create_collection(
            name="aria_memory",
            metadata={"hnsw:space": "cosine"}
        )
    
    def save_memory(self, key: str, content: str, metadata: Dict[str, Any] = None) -> None:
        """
        Save content to memory
        """
        logger.info(f"💾 Saving to memory: {key}")
        
        self.collection.add(
            ids=[key],
            documents=[content],
            metadatas=[metadata or {"type": "general"}]
        )
    
    def retrieve_memory(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant memories
        """
        logger.info(f"🔍 Retrieving from memory: {query}")
        
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        if not results["documents"] or not results["documents"][0]:
            return []
        
        memories = []
        for i, doc in enumerate(results["documents"][0]):
            memories.append({
                "content": doc,
                "similarity": 1 - results["distances"][0][i] if "distances" in results else 0.5,
                "metadata": results["metadatas"][0][i] if "metadatas" in results else {}
            })
        
        return memories
    
    def clear_memory(self) -> None:
        """
        Clear all memories
        """
        logger.warning("🗑️  Clearing all memories...")
        self.client.delete_collection("aria_memory")
        self.collection = self.client.get_or_create_collection(
            name="aria_memory",
            metadata={"hnsw:space": "cosine"}
        )
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics
        """
        count = self.collection.count()
        
        return {
            "total_memories": count,
            "storage_path": str(settings.chroma_db_path),
            "collection_name": "aria_memory"
        }

# Global vector store instance
vector_store = VectorStoreMemory()