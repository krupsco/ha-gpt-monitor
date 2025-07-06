import requests
from datetime import datetime
from utils import log_data

def get_current_state():
    from dotenv import load_dotenv; load_dotenv()
    import os
    HA_URL = os.getenv("HA_URL")
    HA_TOKEN = os.getenv("HA_TOKEN")
    ENTITY_ID = os.getenv("ENTITY_ID")

    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"{HA_URL}/api/states/{ENTITY_ID}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        state = float(data["state"])
        timestamp = datetime.now().isoformat()
        log_data(state, timestamp)
        return {"state": state, "timestamp": timestamp}
    else:
        return None

