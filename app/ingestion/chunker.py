"""
Document chunking with overlap for better retrieval.
"""
import re
from typing import List, Dict

class DocumentChunker:
    """
    Chunk documents into retrievable pieces.
    
    Strategy: Sentence-based chunking with overlap
    - Preserves semantic coherence
    - Overlap ensures context not lost at boundaries
    """
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_by_sentences(self, text: str) -> List[str]:
        """Split text preserving sentence boundaries"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                # Overlap: keep last sentence
                current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def chunk_document(self, doc: Dict) -> List[Dict]:
        """Chunk document into retrievable pieces with metadata"""
        chunks = self.chunk_by_sentences(doc['content'])
        
        return [
            {
                'text': chunk,
                'source': doc['filename'],
                'chunk_id': idx,
                'total_chunks': len(chunks)
            }
            for idx, chunk in enumerate(chunks)
        ]
