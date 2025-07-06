import streamlit as st
from ha import get_current_state
from analyzer import calculate_norms, detect_anomaly
from gpt import interpret_anomaly
import pandas as pd
import os
import json


HA_URL = st.secrets["home_assistant"]["url"]
HA_TOKEN = st.secrets["home_assistant"]["token"]
ENTITY_ID = st.secrets["monitoring"]["entity_id"]
OPENAI_KEY = st.secrets["openai"]["api_key"]

st.title("Monitor energii z Home Assistant + GPT")

data = get_current_state()

if data:
    norm = calculate_norms()

    if norm:
        current_value = data["state"]
        is_anomaly = detect_anomaly(current_value, norm)

        if is_anomaly:
            st.markdown(
                f"<div style='background-color:#ff4b4b;padding:1rem;border-radius:8px;color:white;'>"
                f"<b>Uwaga!</b> Wykryto anomalię: {current_value} (poza zakresem normy)"
                f"</div>",
                unsafe_allow_html=True
            )

            if st.button("Poproś GPT o interpretację"):
                # Załaduj historię
                history_path = "data/history.csv"
                if os.path.exists(history_path):
                    df = pd.read_csv(history_path)
                    history = df["state"].dropna().tolist()
                else:
                    history = []

                explanation = interpret_anomaly(current_value, norm, history)
                st.subheader("Interpretacja GPT:")
                st.write(explanation)
        else:
            st.success(f"Brak anomalii. Aktualna wartość: {current_value}")
    else:
        st.warning("Brak danych historycznych lub nie udało się obliczyć norm.")
else:
    st.warning("Brak danych z Home Assistant.")
