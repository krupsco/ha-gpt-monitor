import pandas as pd
import numpy as np
import json

def calculate_norms(filepath="data/history.csv"):
    df = pd.read_csv(filepath)
    values = df["state"]
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
    return current_value < norm["low"] or current_value > norm["high"]

