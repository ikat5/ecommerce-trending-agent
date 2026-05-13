from db_config import get_engine
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from models import AgentState
import math

# Lightweight multilingual model
embedder = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2') 

def calculate_trend_multiplier(rating, volume_proxy):
    """
    Logarithmic scale for volume to prevent viral items from breaking the math.
    Returns a multiplier (e.g., 1.0 to 1.5) to boost the RRF score.
    """
    if rating is None or volume_proxy is None:
        return 1.0
    
    # Only boost if rating is decent (above 3.5)
    if float(rating) >= 3.5:
        volume_boost = math.log10(float(volume_proxy) + 1) * 0.05 
        return 1.0 + volume_boost
    return 1.0

def hybrid_search_node(state: AgentState):
    engine = get_engine()
    query = state["query"]
    query_vector = embedder.encode(query).tolist()
    
    # EXACT MAPPING BASED ON YOUR PANDAS SCHEMA
    tables = [
        {
            "name": "products", 
            "col_name": "product_name", 
            "col_rating": "average_rating", 
            "col_sold": "rating_count"  # Proxy for volume
        },
        {
            "name": "top_products", 
            "col_name": "product_title", 
            "col_rating": "5.0",  # Literal 5.0 (Assume top products are highly rated)
            "col_sold": "rating_count" # Proxy for volume
        },
        {
            "name": "reviews", 
            "col_name": "product_name", 
            "col_rating": "rating", 
            "col_sold": "0"  # Literal 0 (Reviews table doesn't have volume metrics)
        }
    ]
    
    final_ranked_results = []
    
    for table in tables:
        t_name = table["name"]
        c_name = table["col_name"]
        c_rating = table["col_rating"]
        c_sold = table["col_sold"]
        
        with engine.connect() as conn:
            # 1. Vector Search
            vector_sql = text(f"""
                SELECT {c_name} as name, {c_rating} as rating, {c_sold} as volume_proxy
                FROM {t_name}
                WHERE 1 - (embedding <=> :vector) > 0.35
                ORDER BY embedding <=> :vector LIMIT 20;
            """)
            
            # 2. Keyword/BM25 Search
            keyword_sql = text(f"""
                SELECT {c_name} as name, {c_rating} as rating, {c_sold} as volume_proxy
                FROM {t_name}
                WHERE to_tsvector('english', {c_name}) @@ plainto_tsquery('english', :query_text)
                ORDER BY ts_rank(to_tsvector('english', {c_name}), plainto_tsquery('english', :query_text)) DESC LIMIT 20;
            """)
            
            try:
                vector_rows = conn.execute(vector_sql, {"vector": str(query_vector)}).fetchall()
                keyword_rows = conn.execute(keyword_sql, {"query_text": query}).fetchall()
                
                if vector_rows or keyword_rows:
                    print(f"🎯 Data found in '{t_name}'. Applying Reciprocal Rank Fusion...")
                    
                    product_data = {}
                    rrf_scores = {}
                    k = 60 
                    
                    for rank, row in enumerate(vector_rows):
                        name = row[0]
                        product_data[name] = {"rating": row[1], "volume_proxy": row[2]}
                        rrf_scores[name] = rrf_scores.get(name, 0) + (1 / (k + rank + 1))
                        
                    for rank, row in enumerate(keyword_rows):
                        name = row[0]
                        product_data[name] = {"rating": row[1], "volume_proxy": row[2]}
                        rrf_scores[name] = rrf_scores.get(name, 0) + (1 / (k + rank + 1))
                    
                    for name, base_rrf in rrf_scores.items():
                        rating = product_data[name]["rating"]
                        volume = product_data[name]["volume_proxy"]
                        
                        trend_boost = calculate_trend_multiplier(rating, volume)
                        final_score = base_rrf * trend_boost
                        
                        final_ranked_results.append({
                            "product_name": name,
                            "rating": float(rating) if rating else 0.0,
                            "rank_score": round(final_score, 5),
                            "source": t_name
                        })
                    
                    # Stop searching other tables once we find matches
                    break 

            except Exception as e:
                print(f"⚠️ Skipping '{t_name}' due to error: {e}")
                continue

    # Sort the final list
    sorted_results = sorted(final_ranked_results, key=lambda x: x['rank_score'], reverse=True)[:10]
    
    # Fallback condition for LangGraph Web Search Edge
    needs_web = len(sorted_results) == 0
    
    return {"db_results": sorted_results, "needs_web_search": needs_web}