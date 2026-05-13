from db_config import get_engine
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from models import AgentState

embedder = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2') 

def vector_search_node(state: AgentState):
    engine = get_engine()
    query_vector = embedder.encode(state["query"]).tolist()
    
    # Filter out bad matches with a threshold
    query_sql = text("""
        SELECT product_name, 1 - (embedding <=> :vector) as similarity
        FROM products
        WHERE 1 - (embedding <=> :vector) > 0.35
        ORDER BY embedding <=> :vector
        LIMIT 15;
    """)
    
    results = []
    with engine.connect() as conn:
        rows = conn.execute(query_sql, {"vector": str(query_vector)}).fetchall()
        for row in rows:
            results.append({"name": row[0], "score": float(row[1]), "source": "vector"})
            
    state_results = state.get("db_results", [])
    state_results.extend(results)
    
    return {"db_results": state_results}