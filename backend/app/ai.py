import os
from groq import Groq

# Default me "git" hata kar sirf environment variable check karein
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_document(pdf_text: str, question: str) -> str:
    try:
        truncated_text = pdf_text[:15000] 

        prompt = f"""
        You are a helpful AI assistant. Answer the user's question based ONLY on the provided document text. 
        If the answer is not present in the text, politely state that it's not found in the document.
        
        Document Text:
        {truncated_text}
        
        User Question: {question}
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",  
            temperature=0.3,
        )
        
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Error connecting to Groq AI: {str(e)}"