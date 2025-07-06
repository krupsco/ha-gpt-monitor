import requests
from datetime import datetime
from utils import log_data
import streamlit as st

def get_state_for_entity(entity_id):
    url = st.secrets["home_assistant"]["url"].strip()
    token = st.secrets["home_assistant"]["token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(f"{url}/api/states/{entity_id}", headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Błąd pobierania {entity_id}: {e}")
    return None

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

