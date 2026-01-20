"""
Vector store for document chunks with retrieval.
Keyword-based retrieval with normalization (punctuation-safe).
"""
from typing import List, Dict
import json
import re
from pathlib import Path
from app.agent.schema import DocumentChunk


class VectorStore:
    """
    Document chunk storage with retrieval.

    Current: Keyword-based scoring with token normalization
    Upgrade path:
    - Add embeddings
    - Use cosine similarity
    - Plug in vector DB (Pinecone/Qdrant/etc)
    """

    def __init__(self, store_path: str = "./data/vector_store.json"):
        self.store_path = Path(store_path)
        self.store_path.parent.mkdir(exist_ok=True)
        self.chunks: List[DocumentChunk] = []
        self.load()

    def add_chunks(self, chunks: List[Dict]):
        """Add chunks to store"""
        chunk_objects = [DocumentChunk(**chunk) for chunk in chunks]
        self.chunks.extend(chunk_objects)
        self.save()

    def search(self, query: str, top_k: int = 3) -> List[DocumentChunk]:
        """
        Retrieve most relevant chunks using normalized keyword matching.
        """
        if not self.chunks:
            return []

        # 🔑 Normalize tokens (remove punctuation)
        query_tokens = set(re.findall(r"\w+", query.lower()))

        scored_chunks = []

        for chunk in self.chunks:
            chunk_tokens = set(re.findall(r"\w+", chunk.text.lower()))

            # Keyword overlap score
            overlap_score = len(query_tokens & chunk_tokens)

            # Phrase bonus (still useful)
            phrase_bonus = 5 if query.lower() in chunk.text.lower() else 0

            total_score = overlap_score + phrase_bonus

            if total_score > 0:
                scored_chunks.append((chunk, total_score))

        # Sort by relevance
        scored_chunks.sort(key=lambda x: x[1], reverse=True)

        return [chunk for chunk, _ in scored_chunks[:top_k]]

    def clear(self):
        """Clear all chunks"""
        self.chunks = []
        self.save()

    def save(self):
        """Persist to disk"""
        with open(self.store_path, "w", encoding="utf-8") as f:
            json.dump(
                [
                    {
                        "text": chunk.text,
                        "source": chunk.source,
                        "chunk_id": chunk.chunk_id,
                        "embedding": chunk.embedding,
                    }
                    for chunk in self.chunks
                ],
                f,
                indent=2,
            )

    def load(self):
        """Load from disk"""
        if self.store_path.exists():
            with open(self.store_path, "r", encoding="utf-8") as f:
                chunks_data = json.load(f)
                self.chunks = [DocumentChunk(**chunk) for chunk in chunks_data]

    def get_stats(self) -> Dict:
        """Get store statistics"""
        sources = set(chunk.source for chunk in self.chunks)
        return {
            "total_chunks": len(self.chunks),
            "total_documents": len(sources),
            "sources": list(sources),
        }
