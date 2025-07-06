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

    state = float(data["state"])  # ← najpierw definiujemy state
    save_state_to_history(entity_id, state)  # ← dopiero potem zapisujemy

    unit = data["attributes"].get("unit_of_measurement", "")
    name = data["attributes"].get("friendly_name", "Brak nazwy")

    norm = calculate_norms_for_entity(entity_id)
    is_anomaly = detect_anomaly(state, norm) if norm else False

    card_class = "sensor-card anomaly" if is_anomaly else "sensor-card"

    norm_display = f"{norm['low']} – {norm['high']} {unit}" if norm else "Brak danych"

    with st.container():
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        st.markdown(f"### {name}")
        st.markdown(f"- **Encja:** `{entity_id}`")
        st.markdown(f"- **Aktualna wartość:** `{state} {unit}`")
        st.markdown(f"- **Norma:** {norm_display}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🧠 Interpretuj: {entity_id}"):
                history_path = f"data/{entity_id.replace('.', '_')}_history.csv"
                history = pd.read_csv(history_path)["state"].dropna().tolist() if os.path.exists(history_path) else []
                explanation = interpret_anomaly(state, norm, history)
                st.markdown(f"**GPT:** {explanation}")
        with col2:
            if st.button(f"📈 Historia: {entity_id}"):
                st.markdown("*(Historia jeszcze niezaimplementowana)*")

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
