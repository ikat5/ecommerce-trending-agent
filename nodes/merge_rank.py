from models import AgentState

def merge_rank_node(state: AgentState):
    db_res = state.get("db_results", [])
    needs_web = state.get("needs_web_search", False)
    
    rrf_scores = {}
    vector_list = [item for item in db_res if item['source'] == 'vector']
    keyword_list = [item for item in db_res if item['source'] == 'keyword']
    
    k = 60 
    for rank, item in enumerate(vector_list):
        name = item['name']
        rrf_scores[name] = rrf_scores.get(name, 0) + (1 / (k + rank + 1))
        
    for rank, item in enumerate(keyword_list):
        name = item['name']
        rrf_scores[name] = rrf_scores.get(name, 0) + (1 / (k + rank + 1))
        
    ranked_db_items = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    top_10 = [{"source": "database", "product_name": item[0], "rank_score": round(item[1], 4)} for item in ranked_db_items[:10]]
    
    # DYNAMIC FALLBACK: If DB returned absolutely nothing good, force web search!
    if len(top_10) == 0:
        needs_web = True
        
    return {"merged_results": top_10, "needs_web_search": needs_web}