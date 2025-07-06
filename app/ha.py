import requests
import streamlit as st
import os  # ← TO JEST KLUCZOWE
from datetime import datetime
import csv



def get_state_for_entity(entity_id):
    HA_URL = st.secrets["home_assistant"]["url"].strip()
    HA_TOKEN = st.secrets["home_assistant"]["token"].strip()

    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    url = f"{HA_URL}/api/states/{entity_id}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()

    # Zwracamy również last_updated
    return {
        "state": data.get("state"),
        "attributes": data.get("attributes", {}),
        "last_updated": data.get("last_updated"),
    }


def get_current_state():
    HA_URL = st.secrets["home_assistant"]["url"].strip()
    HA_TOKEN = st.secrets["home_assistant"]["token"].strip()
    ENTITY_ID = st.secrets["monitoring"]["entity_id"].strip()

    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"{HA_URL}/api/states/{ENTITY_ID}", headers=headers)

    if response.status_code == 200:
        data = response.json()
        state = float(data["state"])
        timestamp = datetime.now().isoformat()
        return {"state": state, "timestamp": timestamp}
    else:
        st.error(f"Problem z API HA, kod {response.status_code}")
        return None

    response = requests.get(f"{HA_URL}/api/states/{ENTITY_ID}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        state = float(data["state"])
        timestamp = datetime.now().isoformat()
        log_data(state, timestamp)
        return {"state": state, "timestamp": timestamp}
    else:
        return None

def save_state_to_history(entity_id, state):
    safe_id = entity_id.replace(".", "_")
    filepath = f"data/{safe_id}_history.csv"
    timestamp = datetime.now().isoformat()

    os.makedirs("data", exist_ok=True)

    file_exists = os.path.exists(filepath)
    with open(filepath, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["timestamp", "state"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({"timestamp": timestamp, "state": state})

