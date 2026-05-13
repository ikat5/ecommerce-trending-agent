# Bangladesh E-commerce Trend Intelligence Agent

AI-powered multi-source ecommerce intelligence system focused on Bangladesh market trends.

## What this agent does

This project is a trend-aware recommendation and analysis agent that can:

- detect trending products
- analyze demand and popularity signals
- combine semantic + keyword + hybrid + realtime web retrieval
- scrape Daraz Bangladesh product data for live ecommerce signals
- use Tavily for web search and trend discovery
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
5. `web` (conditional) → Tavily search + Daraz scraping + live trend signals
6. `generate` → final trend-aware response

## Main files

- `app.py` — CLI entrypoint
- `graph.py` — graph workflow and routing
- `models.py` — shared agent state schema
- `llm.py` — Groq LLM configuration
- `nodes/` — node-level pipeline logic
- `dataset/` — CSV data + ingestion utilities
- `database_connection/` — DB connectivity checks
- `nodes/web_search.py` — Tavily search and Daraz scraping

## Data sources used by the agent

- PostgreSQL product tables
- PostgreSQL review tables (expanding in next phase)
- pgvector semantic similarity
- realtime web search signals (trend support)
- Daraz Bangladesh scraping results
- Tavily search results
- hybrid merge/rerank logic

## Setup

### 1) Create/activate virtual environment

```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

### 2) Install dependencies

```bash
pip install langchain langgraph langchain-groq langchain-community sqlalchemy pgvector sentence-transformers pandas psycopg2-binary requests beautifulsoup4 python-dotenv tavily-python
```

### 3) Configure environment variables

Create `.env` in project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
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

## Hybrid search and live ecommerce signals

The system now combines multiple retrieval layers:

- semantic search from pgvector
- keyword matching from PostgreSQL
- hybrid merging and ranking
- Tavily web search for fresh signals
- Daraz Bangladesh scraping for product-level live context

This makes the agent stronger for real Bangladesh ecommerce queries like trending items, price-sensitive recommendations, and category demand checks.

## Bangladesh market focus

The system is tuned for Bangladesh ecommerce context, including local demand behavior, fashion trends, price sensitivity, and seasonal shopping patterns.
