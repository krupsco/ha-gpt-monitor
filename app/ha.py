import requests
from datetime import datetime
from utils import log_data
import streamlit as st


def get_current_state():
    HA_URL = st.secrets["home_assistant"]["url"].strip()
    HA_TOKEN = st.secrets["home_assistant"]["token"].strip()
    ENTITY_ID = st.secrets["monitoring"]["entity_id"].strip()

    st.write(f"DEBUG: HA_URL = '{HA_URL}'")
    st.write(f"DEBUG: ENTITY_ID = '{ENTITY_ID}'")

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

