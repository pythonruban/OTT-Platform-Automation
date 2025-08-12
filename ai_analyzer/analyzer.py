import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # or hardcode the key (not recommended)

def get_ai_suggestion(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're a Python test automation assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )
    return response['choices'][0]['message']['content']