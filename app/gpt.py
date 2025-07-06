import openai
import os

def interpret_anomaly(value, norm, history):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    prompt = f"""Obecna wartość: {value}
Normy: {norm}
Ostatnie wartości: {history[-10:].tolist()}

Czy obecna wartość to anomalia? Jak ją zinterpretować?
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jesteś asystentem do analizy danych z systemu smart home."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
