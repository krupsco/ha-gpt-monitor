import streamlit as st
from ha import get_state_for_entity
from analyzer import calculate_norms_for_entity, detect_anomaly
from gpt import interpret_anomaly
import pandas as pd
import os
from ha import save_state_to_history


st.set_page_config(layout="wide")
st.title("📡 Monitor czujników z Home Assistant + GPT")

entities = st.secrets["monitoring"]["entities"]

# Custom CSS for grid layout
st.markdown("""
    <style>
    .sensor-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 1rem;
    }
    .sensor-card {
        border-radius: 12px;
        padding: 1rem;
        background-color: #f9f9f9;
        border: 1px solid #ddd;
    }
    .sensor-card.anomaly {
        background-color: #ff4b4b !important;
        color: white;
        border: 1px solid #ff0000;
    }
    .sensor-card h4 {
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Begin the grid
st.markdown('<div class="sensor-grid">', unsafe_allow_html=True)

for entity_id in entities:
    data = get_state_for_entity(entity_id)
    if not data:
        continue

    state = float(data["state"])
    save_state_to_history(entity_id, state)

    unit = data["attributes"].get("unit_of_measurement", "")
    name = data["attributes"].get("friendly_name", "Brak nazwy")

    last_updated_iso = data.get("last_updated")
    if last_updated_iso:
        from datetime import datetime
        last_updated_dt = datetime.fromisoformat(last_updated_iso.replace("Z", "+00:00"))
        last_updated_str = last_updated_dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        last_updated_str = "brak danych"

    norm = calculate_norms_for_entity(entity_id)
    is_anomaly = detect_anomaly(state, norm)

    card_class = "sensor-card anomaly" if is_anomaly else "sensor-card"

    norm_display = f"{norm['low']} – {norm['high']} {unit}" if norm else "Brak danych"

    with st.container():
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        st.markdown(f"### {name}")
        st.markdown(f"- **Encja:** `{entity_id}`")
        st.markdown(f"- **Aktualna wartość:** `{state} {unit}`")
        st.markdown(f"- **Norma:** {norm_display}")
        st.markdown(f"- **Ostatnia aktualizacja:** {last_updated_str}")

        # ... tutaj Twoje przyciski itp.

        st.markdown("</div>", unsafe_allow_html=True)

