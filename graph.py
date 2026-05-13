from langgraph.graph import StateGraph, END
from models import AgentState
from nodes.parse_query import parse_query_node
from nodes.vector_search import vector_search_node
from nodes.postgres_search import postgres_search_node
from nodes.Hybrid_search import hybrid_search_node
from nodes.web_search import web_search_node
from nodes.merge_rank import merge_rank_node
from nodes.llm_response import llm_response_node

def should_web_search(state: AgentState):
    """Condition to route to Web Search or straight to Generate"""
    if state.get("needs_web_search"):
        return "web"
    return "generate"

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("parse", parse_query_node)
    workflow.add_node("search_db", hybrid_search_node)
    workflow.add_node("rank", merge_rank_node)
    workflow.add_node("web", web_search_node)
    workflow.add_node("generate", llm_response_node)
    
    workflow.set_entry_point("parse")
    
    # DB Search happens first
    workflow.add_edge("parse", "search_db")
    workflow.add_edge("search_db", "rank")
    
    # CONDITIONAL EDGE: Decide to hit the web or answer directly
    workflow.add_conditional_edges(
        "rank",
        should_web_search,
        {
            "web": "web",
            "generate": "generate"
        }
    )
    
    workflow.add_edge("web", "generate")
    workflow.add_edge("generate", END)
    
    return workflow.compile()