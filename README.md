# RAG video transcript Q&A

A small full-stack app that ingests **one YouTube video’s English captions**, chunks and embeds the transcript, stores vectors in **ChromaDB**, and answers questions via **FastAPI** + **OpenRouter** (LLM). The **React** frontend is a chat UI that calls the backend `/ask` endpoint.

Default source video: [YouTube](https://www.youtube.com/watch?v=qN_2fnOPY-M) (`VIDEO_ID` in `backend/app/config.py`).

---

## Architecture

```
                ┌──────────────────────┐
                │   YouTube Video      │
                │ (English subtitles)  │
                └──────────┬───────────┘
                           │
                           ▼
        ┌──────────────────────────────────┐
        │ Transcript extraction            │
        │ youtube-transcript-api           │
        └──────────┬───────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────────┐
        │ Raw transcript segments          │
        │ (count depends on video; e.g.    │
        │  thousands of caption lines)     │
        └──────────┬───────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────────┐
        │ Windowing (context grouping)     │
        │ WINDOW_SIZE = 10 (config.py)     │
        └──────────┬───────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────────┐
        │ Semantic chunking                │
        │ LangChain SemanticChunker        │
        └──────────┬───────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────────┐
        │ Final text chunks                │
        │ (e.g. ~750+ chunks for sample    │
        │  video after ingestion)          │
        └──────────┬───────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────────┐
        │ Embedding model                  │
        │ BAAI/bge-small-en-v1.5           │
        └──────────┬───────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────────┐
        │ Vector database                  │
        │ ChromaDB (persisted on disk)     │
        └──────────┬───────────────────────┘
                   │
        ┌──────────▼───────────────────────┐
        │         Backend (FastAPI)        │
        │ POST /ask                        │
        └──────────┬───────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────────┐
        │ Retriever (similarity search)    │
        │ Top-K relevant chunks            │
        └──────────┬───────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────────┐
        │ Prompt builder                   │
        │ Transcript context + question    │
        └──────────┬───────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────────┐
        │ LLM (OpenRouter API)             │
        │ Model from config (see below)    │
        └──────────┬───────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────────┐
        │ JSON answer to client            │
        └──────────┬───────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────────┐
        │ Frontend (React + Vite + Tailwind)│
        │ Chat UI + markdown answers       │
        └──────────────────────────────────┘
```

---

## End-to-end request flow

```
User question
     ↓
React frontend (axios → FastAPI)
     ↓
POST /ask
     ↓
Retriever (Chroma similarity search)
     ↓
Relevant transcript chunks
     ↓
Prompt builder (prompts.py)
     ↓
OpenRouter chat completion
     ↓
Generated answer (markdown-capable text)
     ↓
Frontend displays formatted reply
```

---

## Repository layout

```
RAG_Project/
├── README.md
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, CORS, POST /ask
│   │   ├── ingest.py            # Run-once ingestion pipeline entry
│   │   ├── retriever.py         # Load Chroma + similarity search
│   │   ├── rag_chain.py         # OpenRouter client + get_answer()
│   │   ├── prompts.py           # System-style instructions + context
│   │   ├── chunking.py          # Windowing + SemanticChunker
│   │   ├── embeddings.py        # HuggingFace embeddings for chunks + Chroma
│   │   ├── vector_store.py      # Persist documents to ChromaDB
│   │   ├── transcript_loader.py # Fetch captions via youtube-transcript-api
│   │   └── config.py            # API keys, models, VIDEO_ID, paths
│   ├── vector_store/            # Chroma persistence (created after ingest)
│   └── requirements.txt
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    └── src/
        ├── main.jsx
        ├── index.css
        ├── App.jsx
        ├── api.js               # POST http://127.0.0.1:8000/ask
        ├── constants.js         # Source YouTube URL (keep in sync with VIDEO_ID)
        └── components/
            ├── ChatBox.jsx      # Main chat layout + messages
            └── MarkdownBody.jsx # Renders assistant markdown (react-markdown)
```

---

## Configuration

| Item | Location |
|------|-----------|
| YouTube `VIDEO_ID` | `backend/app/config.py` |
| OpenRouter API key | `OPENROUTER_API_KEY` env (see `config.py`) |
| LLM model id | `LLM_MODEL` in `backend/app/config.py` (default `openai/gpt-oss-120b:free`; change to any OpenRouter model you prefer) |
| Embedding model | `EMBEDDING_MODEL` — `BAAI/bge-small-en-v1.5` |
| Caption window size | `WINDOW_SIZE` — `10` |
| Chroma directory | `VECTOR_DB_DIR` — `vector_store` (under `backend/` when running ingest from that cwd) |
| Frontend API base | `frontend/src/api.js` — `http://127.0.0.1:8000` |

Match the **frontend** `YOUTUBE_VIDEO_URL` in `frontend/src/constants.js` with `VIDEO_ID` whenever you change the ingested video.

---

## Quick start

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Set `OPENROUTER_API_KEY` in the environment (or a `.env` file in `backend/` loaded by `python-dotenv`).

Build the vector store (downloads transcript, chunks, embeds, writes Chroma):

```bash
cd backend
python -m app.ingest
```

Run the API:

```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Frontend

Requires a **current Node.js** (Vite 8 expects Node 20.19+ or 22.12+).

```bash
cd frontend
npm install
npm run dev
```

Open the URL Vite prints (usually `http://localhost:5173`).

### 3. API contract

`POST /ask` with JSON body:

```json
{ "question": "Your question about the video transcript" }
```

Response:

```json
{ "question": "...", "answer": "..." }
```

---

## Design notes

- Answers are intended to be **grounded in the ingested transcript**; see `backend/app/prompts.py` for behavior (greetings, off-topic, and “what is this?” meta questions).
- Assistant messages may include **Markdown** (headings, bold, lists); the UI renders them via `react-markdown`.
