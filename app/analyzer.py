import os
import pandas as pd
import json

def calculate_norms_for_entity(entity_id):
    safe_id = entity_id.replace(".", "_")
    filepath = f"data/{safe_id}_history.csv"
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return None

    df = pd.read_csv(filepath)
    if "state" not in df.columns:
        return None

    values = df["state"].dropna()
    return {
        "mean": values.mean(),
        "std": values.std(),
        "low": values.quantile(0.05),
        "high": values.quantile(0.95)
    }

def detect_anomaly(current_value, norm):
    if not norm:
        return False
    return current_value < norm["low"] or current_value > norm["high"]

def calculate_norms(filepath="data/history.csv"):
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        print("Brak danych do analizy – plik jest pusty lub nie istnieje.")
        return None

    try:
        df = pd.read_csv(filepath)
    except pd.errors.EmptyDataError:
        print("Plik jest pusty – brak danych do analizy.")
        return None

    if df.empty or "state" not in df.columns:
        print("Brak danych lub kolumny 'state' w pliku.")
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
        return False
    return current_value < norm["low"] or current_value > norm["high"]
