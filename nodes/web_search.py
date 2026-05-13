from langchain_community.tools import DuckDuckGoSearchResults
from models import AgentState

def web_search_node(state: AgentState):
    search = DuckDuckGoSearchResults()
    print("🌍 Web Search Triggered: Fetching live data...")
    
    # Optimize query for BD ecommerce
    search_query = f"{state['query']} daraz bd price trending"
    results_str = search.run(search_query)
    
    current_merged = state.get("merged_results", [])
    current_merged.append({"source": "live_web_search", "content": results_str})
    
    return {"merged_results": current_merged}