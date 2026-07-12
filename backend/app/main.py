from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import fitz
from app.ai import analyze_document
import os   

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
pdf_text = None  
current_active_file = None  # Naya: Kaunsi file abhi select hai usko track karne ke liye

# Pydantic model dropdown selection ke liye
class SelectDocRequest(BaseModel):
    filename: str

# Paths set up
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Welcome to DocuMind-AI!"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    global pdf_text, current_active_file

    pdf_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded PDF
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Open the PDF and extract text
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        full_text += page.get_text() + "\n"

    # Store globally
    pdf_text = full_text
    current_active_file = file.filename # Upload hote hi isko active set kar diya
    page_count = len(doc)
    doc.close()

    return {
        "message": "PDF uploaded successfully",
        "filename": file.filename,
        "pages": page_count
    }


# 1. NAYA ENDPOINT: Saari uploaded PDFs ki list frontend ko bhejne ke liye
@app.get("/documents")
async def get_documents():
    if not os.path.exists(UPLOAD_DIR):
        return {"documents": [], "active_file": current_active_file}
    
    # Sirf .pdf files ki list nikalenge
    files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith('.pdf')]
    return {"documents": files, "active_file": current_active_file}


# 2. NAYA ENDPOINT: Jab user dropdown se koi purani file select karega
@app.post("/select-document")
async def select_document(req: SelectDocRequest):
    global pdf_text, current_active_file
    
    pdf_path = os.path.join(UPLOAD_DIR, req.filename)
    
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Purani file ko select karke uska text fir se extract kar lenge memory me
    doc = fitz.open(pdf_path)
    full_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        full_text += page.get_text() + "\n"
        
    pdf_text = full_text
    current_active_file = req.filename
    doc.close()
    
    return {"message": f"Active document changed to {req.filename}"}


@app.post("/chat")
async def chat(question: str = Form(...)):
    global pdf_text

    if pdf_text is None:
        return {"error": "Please upload or select a PDF first."}

    answer = analyze_document(pdf_text, question)

    return {
        "question": question,
        "answer": answer
    }