import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Absolute paths to avoid any directory confusion
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "phishing_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "trained_models")
MODEL_PATH = os.path.join(MODEL_DIR, "phishing_v1.joblib")

def train():
    print("\n--- Sentinel AI: Initializing Training Pipeline ---")
    
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    if not os.path.exists(DATA_PATH):
        print(f"CRITICAL ERROR: CSV file not found at {DATA_PATH}")
        return

    # 1. Load Dataset
    df = pd.read_csv(DATA_PATH)
    print(f"SUCCESS: Dataset loaded with {len(df)} rows.")

    # 2. Map Target Column
    # We use 'Result' because that is what is in your CSV.
    if 'Result' in df.columns:
        # Standardize: -1 becomes 0 (Safe), 1 stays 1 (Phishing)
        y = df['Result'].map({-1: 0, 1: 1})
        print("ACTION: Mapped 'Result' column to binary (0/1).")
    else:
        print(f"ERROR: 'Result' column missing! Found: {df.columns.tolist()}")
        return

    # 3. Clean Features
    # We remove 'id' (metadata) and 'Result' (the answer) to get only training data
    cols_to_remove = [c for c in ['id', 'Result'] if c in df.columns]
    X = df.drop(columns=cols_to_remove)
    print(f"ACTION: Training on {X.shape[1]} forensic features.")

    # 4. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Train Random Forest (Optimized for your i5 Processor)
    print("ACTION: Starting Random Forest training (this may take 10-20 seconds)...")
    model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
    model.fit(X_train, y_train)

    # 6. Final Results
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print("\n" + "="*30)
    print(f" FINAL ACCURACY: {acc * 100:.2f}%")
    print("="*30)
    print("\nDetailed Performance Metrics:")
    print(classification_report(y_test, y_pred))

    # 7. Save the Brain
    joblib.dump(model, MODEL_PATH)
    print(f"\nSUCCESS: AI Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()