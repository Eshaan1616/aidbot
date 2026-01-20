from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ConfidenceLevel(str, Enum):
    """Confidence in the answer based on retrieval quality"""
    HIGH = "high"      # Strong match in documentation
    MEDIUM = "medium"  # Partial match
    LOW = "low"        # Weak or no match
    NONE = "none"      # Cannot answer from docs

class SupportAnswer(BaseModel):
    """Structured agent output - enforces grounding"""
    answer: str = Field(
        description="The answer to the user's question, based ONLY on provided documentation"
    )
    confidence: ConfidenceLevel = Field(
        description="Confidence level based on documentation match quality"
    )
    sources: List[str] = Field(
        default_factory=list,
        description="List of source documents used to generate this answer"
    )
    requires_escalation: bool = Field(
        default=False,
        description="True if question cannot be answered from documentation and needs human support"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "To reset your password, go to Settings > Security > Reset Password",
                "confidence": "high",
                "sources": ["user_guide.md"],
                "requires_escalation": False
            }
        }

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    """API response matching SupportAnswer schema"""
    answer: str
    confidence: str
    sources: List[str]
    requires_escalation: bool
    retrieved_chunks: int = Field(description="Number of relevant chunks found")

class DocumentChunk(BaseModel):
    """Single chunk with metadata for retrieval"""
    text: str
    source: str
    chunk_id: int
    total_chunks: Optional[int] = None
    embedding: Optional[List[float]] = None  # For future vector search upgrade

class UploadResponse(BaseModel):
    filename: str
    chunks_created: int
    message: str

class StatsResponse(BaseModel):
    total_chunks: int
    total_documents: int
    sources: List[str]