from pydantic_ai import Agent
from app.ingestion.store import VectorStore


class SupportAgentRunner:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

        self.agent = Agent(
            model="openrouter:meta-llama/llama-3.1-8b-instruct",
            system_prompt=(
                "You are a grounded customer support agent.\n"
                "Answer ONLY using the provided documentation.\n"
                "If the answer is not found, say you don't know."
            ),
        )

    async def answer_question(self, question: str):
        chunks = self.vector_store.search(question)

        context = "\n\n".join(chunk.text for chunk in chunks)

        result = await self.agent.run(
            f"Context:\n{context}\n\nQuestion:\n{question}"
        )

        return (
            {
                "answer": result.output,  # ✅ THIS IS THE RIGHT ONE
                "confidence": "high" if chunks else "low",
                "sources": list({c.source for c in chunks}),
                "requires_escalation": not bool(chunks),
            },
            chunks,
        )
