from llm import get_llm
from models import AgentState
from langchain_core.prompts import ChatPromptTemplate

def llm_response_node(state: AgentState):
    llm = get_llm()
    context = "\n".join([str(item) for item in state.get("merged_results", [])])
    
    prompt = ChatPromptTemplate.from_template(
        "You are a Senior AI Ecommerce expert for Bangladesh.\n"
        "User Query: {query}\n\n"
        "Retrieved Data Context (From Database & Web):\n{context}\n\n"
        "STRICT INSTRUCTIONS:\n"
        "1. Analyze the context carefully. If the user asked for a 'Mobile Phone' but the database only returned 'Mobile Stands' or 'Covers', DO NOT recommend the stands as phones. Explicitly point out they are just accessories.\n"
        "2. If the database lacks the exact product (like trending t-shirts or phones), rely entirely on the 'live_web_search' data or your own expert knowledge of Bangladesh e-commerce to recommend real products.\n"
        "3. If the user asked in Bangla or Banglish, reply naturally in that language. Be highly accurate and helpful."
    )
    
    chain = prompt | llm
    response = chain.invoke({"query": state["query"], "context": context})
    
    return {"final_response": response.content}