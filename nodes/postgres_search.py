from db_config import get_engine
from sqlalchemy import text
from models import AgentState

def postgres_search_node(state: AgentState):
    engine = get_engine()
    query_sql = text("""
        SELECT product_name
        FROM products
        WHERE product_name ILIKE :keyword
        LIMIT 10;
    """)
    
    keyword = f"%{state['query']}%"
    results = []
    with engine.connect() as conn:
        rows = conn.execute(query_sql, {"keyword": keyword}).fetchall()
        for row in rows:
            results.append({"name": row[0], "score": 1.0, "source": "keyword"})
            
    state_results = state.get("db_results", [])
    state_results.extend(results)
    
    return {"db_results": state_results}