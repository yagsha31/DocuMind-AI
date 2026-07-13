import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

MODEL = "qwen2.5:3b"


def analyze_document(pdf_text: str, question: str):

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY from the uploaded document.

If the answer is not found, say:
"I could not find this information in the uploaded document."

Document:
{pdf_text[:15000]}

Question:
{question}
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()["response"]

    except Exception as e:

        return f"Ollama Error: {str(e)}"