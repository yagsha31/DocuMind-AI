import os
import traceback
from groq import Groq

def analyze_document(pdf_text: str, question: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "Error: GROQ_API_KEY not found."

    try:
        client = Groq(
            api_key=api_key,
            timeout=60
        )

        prompt = f"""
You are a helpful AI assistant.

Answer ONLY from the uploaded document.

If the answer is not available in the document, reply:
'I could not find this information in the uploaded document.'

Document:
{pdf_text[:15000]}

Question:
{question}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        traceback.print_exc()
        return f"Groq Error: {str(e)}"