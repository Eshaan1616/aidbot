from fastapi import APIRouter, HTTPException
from app.agent.schema import ChatRequest, ChatResponse
from app.agent.support_agent import SupportAgentRunner
from app.ingestion.store import VectorStore

router = APIRouter()

vector_store = VectorStore()
agent_runner = SupportAgentRunner(vector_store)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result, chunks_used = await agent_runner.answer_question(request.message)

        return ChatResponse(
            answer=result["answer"],
            confidence=result["confidence"],
            sources=result["sources"],
            requires_escalation=result["requires_escalation"],
            retrieved_chunks=len(chunks_used),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")
