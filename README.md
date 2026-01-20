🚀 AidBot
Grounded AI Customer Support Platform

AidBot is a retrieval-augmented, document-grounded AI support system built for SaaS and enterprise environments where accuracy, explainability, and control are non-negotiable.

❗ Unlike generic AI chatbots, AidBot does not rely on pretrained knowledge.
Every response is generated only from uploaded documentation via retrieval.

This makes AidBot suitable for customer support, internal enablement, and regulated domains.

🎯 Core Design Principle
No grounding → no answer

The agent never answers from memory

All responses are derived from retrieved document chunks

If documentation does not contain the answer, the system explicitly signals escalation

AidBot is not a chatbot — it is a knowledge-grounded enterprise support system.

🏗️ System Architecture
User Question
     ↓
Retrieval (Top-K document chunks)
     ↓
Grounded Agent (PydanticAI)
     ↓
Structured Output (SupportAnswer schema)
     ↓
API Response (answer + confidence + sources)

🧠 Key Components
1️⃣ Agent

app/agent/support_agent.py

Built using PydanticAI

Strict system prompt enforces documentation-only answers

Agent only sees retrieved chunks as context

Produces validated, structured output

2️⃣ Retrieval Layer

app/ingestion/store.py

Keyword-based retrieval (intentionally dependency-light)

Top-K retrieval executed for every query

No answer is generated without retrieved context

3️⃣ Structured Output

app/agent/schema.py

SupportAnswer schema enforces output shape

Fields include:

answer

confidence (HIGH / MEDIUM / LOW / NONE)

sources

requires_escalation

Prevents hallucination and unstructured responses

4️⃣ Document Processing

Sentence-based chunking with overlap

Metadata tracking (source, chunk id)

Persistent JSON-based storage (upgrade-ready)

📁 Project Structure
aidbot-project/
├── app/
│   ├── agent/
│   │   ├── schema.py          # Pydantic schemas (SupportAnswer)
│   │   └── support_agent.py   # Grounded PydanticAI agent ⭐
│   ├── ingestion/
│   │   ├── loader.py          # Document loading
│   │   ├── chunker.py         # Text chunking
│   │   ├── store.py           # Retrieval layer
│   │   └── embeddings.py     # Upgrade stub (semantic search)
│   ├── api/
│   │   ├── upload.py          # Document upload endpoints
│   │   └── chat.py            # Agent execution endpoint ⭐
│   └── main.py                # FastAPI application
│
├── frontend/
│   └── src/
│       └── components/
│           ├── AidBot.jsx
│           ├── Landing.jsx
│           ├── SystemOverview.jsx
│           ├── AnswerCard.jsx
│           ├── Documents.jsx
│           └── Status.jsx
│
├── requirements.txt
└── README.md

🌐 Frontend Capabilities

The frontend is designed to expose system behavior, not hide it.

Users can clearly see:

Whether documentation has been uploaded

How much knowledge is indexed

When the agent can or cannot answer

Confidence and escalation signals

This transparency is critical for enterprise trust.

🔌 API Endpoints
📄 Upload Documentation
POST /api/upload

{
  "filename": "support_docs.txt",
  "chunks_created": 12,
  "message": "Successfully processed support_docs.txt"
}

💬 Ask a Question
POST /api/chat

{
  "message": "How do I reset my password?"
}

{
  "answer": "To reset your password, go to Settings > Security...",
  "confidence": "high",
  "sources": ["user_guide.md"],
  "requires_escalation": false,
  "retrieved_chunks": 3
}

📊 Document Status
GET /api/documents


Returns document count, chunk count, and sources.

❤️ Health Check
GET /health

🚀 Running the Platform
Backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Frontend
cd frontend
npm install
npm run dev

🏢 SaaS & Enterprise Use Cases
📡 Telecom & ISP Platforms

Reduce customer support load

Answer billing, plan, and policy questions accurately

Improve first-contact resolution

Reduce customer churn caused by misinformation

🧩 Customer Support SaaS

Replace static FAQs with grounded AI assistance

Ensure consistent answers across support channels

Assist support agents with verified responses

🧱 B2B SaaS Products

Product documentation assistants

API and integration support bots

Internal enablement tools for sales and onboarding teams

⚖️ Regulated Domains

Finance, healthcare, legal, compliance

Environments where hallucination is unacceptable

Systems requiring traceability and auditability

🔒 Production Considerations

File type validation on upload

Size limits (configurable)

Full Pydantic validation across boundaries

Async-safe FastAPI routes

Clear separation of ingestion, retrieval, and generation

🔄 Upgrade Paths

Current implementation intentionally avoids heavy dependencies.

Planned / Easy upgrades:

Semantic search (sentence-transformers)

Vector databases (Pinecone, Qdrant, Weaviate)

Multi-turn conversation memory

PDF and multimodal document support

Multi-tenant SaaS deployment

📜 License

MIT