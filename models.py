from typing import List, Dict, Any, TypedDict

class AgentState(TypedDict):
    query: str
    needs_web_search: bool
    db_results: List[Dict[str, Any]]
    web_results: List[Dict[str, Any]]
    merged_results: List[Dict[str, Any]]
    final_response: str