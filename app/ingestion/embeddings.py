"""
Embedding generation for semantic search.
Currently using simple keyword matching, but structured for easy upgrade to:
- Sentence Transformers
- OpenAI embeddings
- Cohere embeddings

NOTE: This is a stub for future enhancement. Currently keyword-based 
retrieval in store.py is used. This module exists to show upgrade path.
"""
from typing import List

class EmbeddingService:
    """
    Handles text embedding generation.
    Currently: NOT USED (keyword-based retrieval in VectorStore)
    Future upgrade path: Integrate sentence-transformers or API embeddings
    """
    
    def __init__(self, method: str = "keyword"):
        self.method = method
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding - placeholder for future implementation"""
        raise NotImplementedError(
            "Embeddings not yet implemented. Using keyword search. "
            "See VectorStore.search() for current retrieval method."
        )