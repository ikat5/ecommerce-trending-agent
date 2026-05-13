import pandas as pd
import numpy as np
import os

# =========================
# Get current directory
# =========================
current_dir = os.path.dirname(os.path.abspath(__file__))

# =========================
# Dataset path
# =========================
dataset_path = os.path.join(current_dir, 'db_ready_products.csv')

print(f"Looking for dataset at: {dataset_path}")

if os.path.exists(dataset_path):

    # =========================
    # Load dataset
    # =========================
    df = pd.read_csv(dataset_path)

    

else:
    print(f"Error: raw.csv not found at {dataset_path}")