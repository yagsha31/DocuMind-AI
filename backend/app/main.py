import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
from groq import Groq

app = FastAPI()

# CORS configuration to allow your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production me aap ise specific frontend URL de sakti hain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq Client Initialization (Fixed Line)
# Default "git" string hata diya hai taaki Render ki Environment Variable automatic pick ho sake
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# In-memory storage for simplicity
UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

db = {
    "documents": [],
    "active_file": None,
    "extracted_text": ""
}

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

        # Llama 3.3 Versatile model
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

@app.get("/")
def read_root():
    return {"message": "Welcome to DocuMind AI Backend!"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Extract text from PDF
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse PDF: {str(e)}")
    
    # Update local state
    if file.filename not in db["documents"]:
        db["documents"].append(file.filename)
    db["active_file"] = file.filename
    db["extracted_text"] = text

    return {"message": f"File '{file.filename}' uploaded and processed successfully."}

@app.get("/documents")
def get_documents():
    return {
        "documents": db["documents"],
        "active_file": db["active_file"]
    }

@app.post("/select-document")
def select_document(payload: dict):
    filename = payload.get("filename")
    if filename not in db["documents"]:
        raise HTTPException(status_code=404, detail="Document not found in history.")
    
    file_path = os.path.join(UPLOAD_DIR, filename)
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")
        
    db["active_file"] = filename
    db["extracted_text"] = text
    return {"message": f"Active document changed to '{filename}'"}

@app.post("/chat")
def chat(question: str = Form(...)):
    if not db["active_file"] or not db["extracted_text"]:
        raise HTTPException(status_code=400, detail="No active document found. Please upload a PDF first.")
    
    answer = analyze_document(db["extracted_text"], question)
    return {"answer": answer}