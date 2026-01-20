"""
FastAPI application entry point.
"""
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload, chat

app = FastAPI(
    title="Grounded AI Support Agent",
    description="Enterprise customer support agent with retrieval-grounded responses",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api", tags=["Documents"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/")
async def root():
    return {
        "message": "Grounded AI Support Agent",
        "architecture": "Retrieval-Augmented Generation (RAG)",
        "grounding": "All responses from uploaded documentation only"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
