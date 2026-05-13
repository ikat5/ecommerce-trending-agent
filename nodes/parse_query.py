from llm import get_llm
from models import AgentState
from langchain_core.prompts import ChatPromptTemplate

def parse_query_node(state: AgentState):
    query = state["query"].lower()
    
    # 1. Rule-based override: Always web search for these keywords
    trigger_words = ["trend", "best sell", "best selling", "popular", "top", "demanding"]
    if any(word in query for word in trigger_words):
        return {"needs_web_search": True, **state}
        
    # 2. Otherwise, let LLM decide
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        "Analyze this ecommerce query: '{query}'. "
        "Does it ask for very recent news or current viral trends? "
        "Reply with ONLY 'true' or 'false'."
    )
    chain = prompt | llm
    response = chain.invoke({"query": state["query"]}).content.strip().lower()
    
    needs_web = "true" in response
    return {"needs_web_search": needs_web, **state}