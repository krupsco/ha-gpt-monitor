import os
import pandas as pd
import json
from datetime import datetime
import pytz

tz = pytz.timezone("Europe/Warsaw")
now = datetime.now(tz)

st.write(f"Obecny czas lokalny: {now.strftime('%Y-%m-%d %H:%M:%S')}")

def calculate_norms_for_entity(entity_id):
    safe_id = entity_id.replace(".", "_")
    filepath = f"data/{safe_id}_history.csv"
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        print(f"Brak danych dla {entity_id}")
        return None

    df = pd.read_csv(filepath)
    if df.empty or "state" not in df.columns or "timestamp" not in df.columns:
        print(f"Brak wymaganych kolumn w historii {entity_id}")
        return None

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["hour"] = df["timestamp"].dt.hour

    grouped = df.groupby(["day_of_week", "hour"])["state"].agg(
        mean="mean",
        std="std",
        low=lambda x: x.quantile(0.05),
        high=lambda x: x.quantile(0.95)
    ).reset_index()

    norm_dict = {}
    for _, row in grouped.iterrows():
        key = f"{int(row['day_of_week'])}_{int(row['hour'])}"  # klucz jako string
        norm_dict[key] = {
            "mean": row["mean"],
            "std": row["std"],
            "low": row["low"],
            "high": row["high"]
        }

    norm_file = f"data/{safe_id}_norms.json"
    with open(norm_file, "w") as f:
        json.dump(norm_dict, f)

    return norm_dict

    # Konwersja na słownik do szybkiego wyszukiwania normy
    norm_dict = {}
    for _, row in grouped.iterrows():
        key = (int(row["day_of_week"]), int(row["hour"]))
        norm_dict[key] = {
            "mean": row["mean"],
            "std": row["std"],
            "low": row["low"],
            "high": row["high"]
        }

    # Zapis norm do pliku JSON
    norm_file = f"data/{safe_id}_norms.json"
    with open(norm_file, "w") as f:
        json.dump(norm_dict, f)

    return norm_dict

def detect_anomaly(current_value, norm_dict):
    if norm_dict is None:
        return False

    now = datetime.now()
    key = f"{now.weekday()}_{now.hour}"

    norm = norm_dict.get(key)
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

def detect_anomaly(current_value, norm_dict):
    if norm_dict is None:
        return False

    now = datetime.now(tz)  # Ustawiona strefa czasowa z pytz
    key = f"{now.weekday()}_{now.hour}"

    norm = norm_dict.get(key)
    if not norm:
        return False

    return current_value < norm["low"] or current_value > norm["high"]
