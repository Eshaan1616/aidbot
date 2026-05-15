# AidBot

AidBot is a grounded support assistant with:

- FastAPI for upload, indexing, and chat APIs
- React + Vite frontend for document and chat workflows
- ChromaDB as the persistent vector database
- Local sentence-transformers embeddings for semantic retrieval
- PydanticAI for answer generation using retrieved context only

## What Changed

The original hackathon version used JSON-backed keyword overlap and optimistic confidence labels. This version now:

- stores chunks in a real vector database instead of `data/vector_store.json`
- generates semantic embeddings locally for chunk indexing and query search
- exposes retrieval score, embedding model, and vector backend in the API
- derives confidence from retrieval similarity instead of hardcoded labels
- fixes broken `.env.example` files
- fixes the frontend API base URL configuration bug
- tightens upload filename handling and CORS configuration

## Backend Setup

Create a `.env` file in the repo root with values like:

```env
OPENROUTER_API_KEY=your-openrouter-api-key
LLM_MODEL=openrouter:meta-llama/llama-3.1-8b-instruct
VECTOR_DB_PATH=./data/chroma
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Then install and run:

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend Setup

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

Then run:

```powershell
cd frontend
npm install
npm run dev
```

## Deployment Setup

For an interview-safe deployment, this project is best split into:

- frontend on Vercel
- backend on Render with persistent disk

Why: the backend stores uploads, Chroma data, users, sessions, and conversations on disk. That works well on a persistent backend host, but is not a good fit for Vercel serverless functions.

### Backend on Render

This repo now includes [render.yaml](C:\Users\eshaa\OneDrive\Desktop\aidbot-project\render.yaml) for the backend service. It configures:

- `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- a persistent disk mounted at `/var/data`
- env-backed paths for uploads, vectors, users, sessions, and conversations

Important:

- set `OPENROUTER_API_KEY` in Render
- replace `ALLOWED_ORIGINS` with your real Vercel frontend URL

### Frontend on Vercel

Deploy the [frontend](C:\Users\eshaa\OneDrive\Desktop\aidbot-project\frontend) directory as the Vercel project root and set:

```env
VITE_API_URL=https://your-backend.onrender.com
```

The frontend also includes [vercel.json](C:\Users\eshaa\OneDrive\Desktop\aidbot-project\frontend\vercel.json) so Vercel detects it as a Vite app cleanly.

## API Endpoints

- `POST /api/upload` uploads and indexes `.txt` and `.md` files
- `GET /api/documents` returns indexed document stats plus vector backend metadata
- `DELETE /api/documents` clears the active collection
- `POST /api/chat` runs retrieval + grounded generation
- `GET /health` returns API health and current vector indexing status

## Notes

- Existing `data/vector_store.json` is now legacy and no longer used.
- Embeddings run locally with `all-MiniLM-L6-v2`, so no embedding API key is required.
- Uploaded documents and vector data are local development state and should not be treated as source-controlled truth.
- There is no production database in this repo; persistence is file-based by design.
