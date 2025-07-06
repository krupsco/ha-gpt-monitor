import pandas as pd
import numpy as np
import json
import os

def calculate_norms(filepath="data/history.csv"):
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        print("Brak danych do analizy – plik pusty lub nie istnieje.")
        return None

    df = pd.read_csv(filepath)
    if "state" not in df.columns or df.empty:
        print("Brak kolumny 'state' lub dane są puste.")
        return None

    values = df["state"].dropna()
    norm = {
        "mean": values.mean(),
        "std": values.std(),
        "low": values.quantile(0.05),
        "high": values.quantile(0.95)
    }

    with open("data/norms.json", "w") as f:
        json.dump(norm, f)

    return norm

def detect_anomaly(current_value, norm):
    if norm is None:
        # brak norm do porównania, więc nie wykrywamy anomalii
        return False
    return current_value < norm["low"] or current_value > norm["high"]
