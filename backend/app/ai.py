import os
from groq import Groq

# Groq Client ko initialize karein
client = Groq(api_key=os.environ.get("GROQ_API_KEY",""))

def analyze_document(pdf_text: str, question: str) -> str:
    try:
        # Rate limit aur heavy files se bachne ke liye safe text limit
        truncated_text = pdf_text[:15000] 

        prompt = f"""
        You are a helpful AI assistant. Answer the user's question based ONLY on the provided document text. 
        If the answer is not present in the text, politely state that it's not found in the document.
        
        Document Text:
        {truncated_text}
        
        User Question: {question}
        """

        # Llama 3.3 Versatile sabse stable aur powerful model hai
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",  # <-- Ekdam sahi aur stable model name
            temperature=0.3,
        )
        
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Error connecting to Groq AI: {str(e)}"