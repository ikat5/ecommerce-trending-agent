from graph import build_graph
import warnings

# Suppress annoying huggingface warnings
warnings.filterwarnings("ignore")

def main():
    agent = build_graph()
    print("🚀 Lightweight E-Trending Agent Online! Type 'exit' to quit.")
    
    while True:
        user_query = input("\nUser: ")
        if user_query.lower() == 'exit':
            break
            
        inputs = {
            "query": user_query,
            "needs_web_search": False,
            "db_results": [],
            "web_results": [],
            "merged_results": [],
            "final_response": ""
        }
        
        try:
            print("Thinking...")
            result = agent.invoke(inputs)
            print("\n🤖 Agent:\n" + result["final_response"])
        except Exception as e:
            print(f"\n❌ Error occurred: {e}")

if __name__ == "__main__":
    main()