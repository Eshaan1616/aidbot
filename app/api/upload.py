"""
Document upload and management endpoints.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ingestion.loader import DocumentLoader
from app.ingestion.chunker import DocumentChunker
from app.ingestion.store import VectorStore
from app.agent.schema import UploadResponse, StatsResponse

router = APIRouter()

loader = DocumentLoader()
chunker = DocumentChunker()
vector_store = VectorStore()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process document into chunks"""
    try:
        if not file.filename.endswith(('.txt', '.md')):
            raise HTTPException(400, "Only .txt and .md files supported")
        
        # Security: Check file size (max 10MB)
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(400, "File too large. Maximum size is 10MB")
        
        file_path = loader.save_upload(file.filename, content)
        
        doc = loader.load_text_file(file_path)
        chunks = chunker.chunk_document(doc)
        
        vector_store.add_chunks(chunks)
        
        return UploadResponse(
            filename=file.filename,
            chunks_created=len(chunks),
            message=f"Successfully processed {file.filename}"
        )
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/documents", response_model=StatsResponse)
async def get_documents():
    """Get knowledge base statistics"""
    stats = vector_store.get_stats()
    return StatsResponse(**stats)

@router.delete("/documents")
async def clear_documents():
    """Clear all documents"""
    vector_store.clear()
    return {"message": "All documents cleared"}
