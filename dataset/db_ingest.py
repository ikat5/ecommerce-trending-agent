
#db_ingest.py
import pandas as pd
from sqlalchemy import text
from pgvector.sqlalchemy import Vector
from sentence_transformers import SentenceTransformer
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db_config import get_engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# --- HELPER FUNCTION: SETUP ---
def setup_database(engine):
    """Ensures the pgvector extension is enabled."""
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    print("✅ Database extension 'vector' is ready.")

# --- FUNCTION 1: PRODUCTS ---
def process_products(engine, model):
    print("\n--- Processing Products ---")
    df = pd.read_csv(os.path.join(BASE_DIR, 'db_ready_products.csv'))
    df['combined_text'] = df['combined_text'].fillna('')
    df['product_name'] = df['product_name'].fillna('Unknown')
    
    print("Generating embeddings for products...")
    df['embedding'] = df['combined_text'].apply(lambda x: model.encode(x).tolist())
    
    df = df.drop(columns=['combined_text', 'product_description'])
    df.to_sql('products', engine, if_exists='replace', index=False,
              dtype={'embedding': Vector(384)})
    print("✅ 'products' table updated.")

# --- FUNCTION 2: TOP PRODUCTS ---
def process_top_products(engine, model):
    print("\n--- Processing Top Products ---")
    df_top = pd.read_csv(os.path.join(BASE_DIR, 'db_ready_top_products.csv'))
    df_top['combined_text'] = df_top['combined_text'].fillna('')
    df_top['product_title'] = df_top['product_title'].fillna('Unknown')
    
    print("Generating embeddings for top products...")
    df_top['embedding'] = df_top['combined_text'].apply(lambda x: model.encode(x).tolist())
    
    df_top = df_top.drop(columns=['combined_text'])
    df_top.to_sql('top_products', engine, if_exists='replace', index=False,
                  dtype={'embedding': Vector(384)})
    print("✅ 'top_products' table updated.")

# --- FUNCTION 3: REVIEWS ---
def process_reviews(engine, model):
    print("\n--- Processing Reviews ---")
    df_reviews = pd.read_csv(os.path.join(BASE_DIR, 'db_ready_reviews.csv'))
    df_reviews['combined_text'] = df_reviews['combined_text'].fillna('')
    df_reviews['review'] = df_reviews['review'].fillna('')
    
    print("Generating embeddings for reviews...")
    df_reviews['embedding'] = df_reviews['combined_text'].apply(lambda x: model.encode(x).tolist())
    
    df_reviews = df_reviews.drop(columns=['combined_text'])
    df_reviews.to_sql('reviews', engine, if_exists='replace', index=False,
                      dtype={'embedding': Vector(384)})
    print("✅ 'reviews' table updated.")

# --- MAIN EXECUTION BLOCK ---
def main():
    # 1. Start Engine and Load Model (Only once!)
    engine = get_engine()
    
    # In your db_ingest.py
    print("Loading Hugging Face model (paraphrase-multilingual-MiniLM-L12-v2)...")
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    
    # 2. Run Setup
    setup_database(engine)
    
    # 3. Call the three functions
    try:
        process_products(engine, model)
        process_top_products(engine, model)
        process_reviews(engine, model)
        print("\n🚀 ALL DATA SUCCESSFULLY STORED!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()