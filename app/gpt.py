from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def interpret_anomaly(current_value, norm, history):
    prompt = f"""
    Dane z czujnika energii wykazują odchylenie od normy.

    Obecny odczyt: {current_value}
    Średnia: {norm['mean']}, Odchylenie standardowe: {norm['std']}
    Zakres typowy: {norm['low']} - {norm['high']}
    Ostatnie odczyty: {history[-5:]}
    
    Wytłumacz, co może być przyczyną odchylenia.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jesteś pomocnym analitykiem danych czujnikowych."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
