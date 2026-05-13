# Bangladesh E-commerce Trend Intelligence Agent

AI-powered multi-source ecommerce intelligence system focused on Bangladesh market trends.

## What this agent does

This project is a trend-aware recommendation and analysis agent that can:

- detect trending products
- analyze demand and popularity signals
- combine semantic + keyword + web trend retrieval
- support Bangla, Banglish, and English user queries
- explain why a product is trending with evidence-based reasoning

## Current scope

- ✅ Trending result pipeline implemented
- 🔜 Product review analysis pipeline (next phase)

## Project architecture

The runtime flow is built with LangGraph:

1. `parse` → query intent + web-search decision
2. `vector_db` → pgvector semantic retrieval
3. `keyword_db` → PostgreSQL keyword retrieval
4. `rank` → reciprocal-rank fusion (RRF) merge
5. `web` (conditional) → realtime web signal retrieval
6. `generate` → final trend-aware response

## Main files

- `app.py` — CLI entrypoint
- `graph.py` — graph workflow and routing
- `models.py` — shared agent state schema
- `llm.py` — Groq LLM configuration
- `nodes/` — node-level pipeline logic
- `dataset/` — CSV data + ingestion utilities
- `database_connection/` — DB connectivity checks

## Data sources used by the agent

- PostgreSQL product tables
- PostgreSQL review tables (expanding in next phase)
- pgvector semantic similarity
- realtime web search signals (trend support)
- hybrid merge/rerank logic

## Setup

### 1) Create/activate virtual environment

```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

### 2) Install dependencies

```bash
pip install langchain langgraph langchain-groq langchain-community sqlalchemy pgvector sentence-transformers pandas psycopg2-binary duckduckgo-search
```

### 3) Configure environment variables

Create `.env` in project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4) Configure database

Update DB credentials in `db_config.py` (and `dataset/db_config.py` if used for ingestion).

### 5) Run the agent

```bash
python3 app.py
```

## Notes

- Keep secrets only in `.env` (never hardcode API keys).
- `.gitignore` is configured to keep virtual env files, caches, and secrets out of Git.
- Recommended before push:

```bash
git add .
git status
```

## Bangladesh market focus

The system is tuned for Bangladesh ecommerce context, including local demand behavior, fashion trends, price sensitivity, and seasonal shopping patterns.
