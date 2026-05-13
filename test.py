import pandas as pd
import numpy as np
import os
import uuid
from datetime import datetime

# =========================
# Get current directory
# =========================
current_dir = os.path.dirname(os.path.abspath(__file__))

# =========================
# Dataset path
# =========================
dataset_path = os.path.join(
    current_dir,
    'dataset.csv'
)

print(f"Looking for dataset at: {dataset_path}")

if os.path.exists(dataset_path):

    # =========================
    # Load dataset
    # =========================
    df = pd.read_csv(dataset_path)

    print("Original Shape:", df.shape)

    # =========================
    # Remove unwanted column
    # =========================
    df = df.drop(
        columns=['Data Source'],
        errors='ignore'
    )

    # =========================
    # Rename columns
    # PostgreSQL friendly
    # =========================
    df.columns = [
        'rating',
        'review',
        'product_name',
        'product_category',
        'emotion',
        'sentiment'
    ]

    # =========================
    # Remove duplicates
    # =========================
    df = df.drop_duplicates()

    # Remove duplicate reviews
    df = df.drop_duplicates(
        subset=['review']
    )

    # =========================
    # Remove empty rows
    # =========================
    df = df.dropna(how='all')

    # =========================
    # Clean text columns
    # =========================
    text_cols = [
        'review',
        'product_name',
        'product_category'
    ]

    for col in text_cols:

        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.replace(r'\s+', ' ', regex=True)
        )

    # =========================
    # Fill missing values
    # =========================
    df['review'] = df['review'].fillna(
        'No Review'
    )

    df['product_name'] = df['product_name'].fillna(
        'Unknown Product'
    )

    df['product_category'] = df[
        'product_category'
    ].fillna(
        'Unknown Category'
    )

    # =========================
    # Encode sentiment
    # =========================
    sentiment_map = {
        'Positive': 1,
        'Negative': 0
    }

    df['sentiment'] = df[
        'sentiment'
    ].map(sentiment_map)

    # =========================
    # Encode emotion
    # =========================
    emotion_map = {
        'Happy': 1,
        'Love': 2,
        'Sadness': 3,
        'Fear': 4,
        'Anger': 5
    }

    df['emotion'] = df[
        'emotion'
    ].map(emotion_map)

    # =========================
    # Convert rating
    # =========================
    df['rating'] = pd.to_numeric(
        df['rating'],
        errors='coerce'
    ).fillna(0)

    # =========================
    # Remove invalid sentiment
    # =========================
    df = df.dropna(
        subset=['sentiment']
    )

    # =========================
    # Generate UUID
    # =========================
    df['review_id'] = [
        str(uuid.uuid4())
        for _ in range(len(df))
    ]

    # =========================
    # Review score
    # Useful for ranking
    # =========================
    df['review_score'] = (
        (df['rating'] * 0.7) +
        (df['sentiment'] * 0.3)
    )

    # =========================
    # Combined text
    # VectorDB ready
    # =========================
    df['combined_text'] = (
        'Product: ' +
        df['product_name'] +
        ' | Category: ' +
        df['product_category'] +
        ' | Review: ' +
        df['review']
    )

    # =========================
    # Timestamp
    # =========================
    df['created_at'] = datetime.now()

    # =========================
    # Reorder columns
    # =========================
    df = df[
        [
            'review_id',
            'product_name',
            'product_category',
            'review',
            'rating',
            'sentiment',
            'emotion',
            'review_score',
            'combined_text',
            'created_at'
        ]
    ]

    # =========================
    # Sort by review score
    # =========================
    df = df.sort_values(
        by='review_score',
        ascending=False
    )

    # =========================
    # Reset index
    # =========================
    df = df.reset_index(drop=True)

    # =========================
    # Save cleaned dataset
    # =========================
    cleaned_path = os.path.join(
        current_dir,
        'db_ready_reviews.csv'
    )

    df.to_csv(cleaned_path, index=False)

    # =========================
    # Output
    # =========================
    print("\nCleaned Shape:", df.shape)

    print(
        f"\nDatabase-ready dataset saved at:\n{cleaned_path}"
    )

    print("\nFinal Columns:\n")
    print(df.columns.tolist())

    print("\nPreview:\n")
    print(df.head())

else:
    print(
        f"Error: dataset.csv not found at {dataset_path}"
    )