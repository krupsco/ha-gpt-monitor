import streamlit as st



from ha import get_current_state
from analyzer import calculate_norms, detect_anomaly
from gpt import interpret_anomaly
import pandas as pd

HA_URL = st.secrets["home_assistant"]["url"]
HA_TOKEN = st.secrets["home_assistant"]["token"]
ENTITY_ID = st.secrets["monitoring"]["entity_id"]
OPENAI_KEY = st.secrets["openai"]["api_key"]

st.title("Monitor energii z Home Assistant + GPT")

data = get_current_state()
if data:
    norm = calculate_norms()
    is_anomaly = detect_anomaly(data["state"], norm)

    st.metric("Aktualna moc", f"{data['state']} W")
    st.write(f"Zakres normy: {round(norm['low'],1)}–{round(norm['high'],1)} W")

    if is_anomaly:
        history = pd.read_csv("data/history.csv")["state"]
        explanation = interpret_anomaly(data["state"], norm, history)
        st.error("Wykryto anomalię!")
        st.write(explanation)
    else:
        st.success("Brak odchyleń od normy.")
else:
    st.error("Nie udało się pobrać danych.")
