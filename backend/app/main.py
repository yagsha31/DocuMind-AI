import os
import fitz

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.ai import analyze_document

app = FastAPI(title="DocuMind AI Backend")

# ---------------- CORS ---------------- #

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://YOUR-FRONTEND-URL.onrender.com",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Upload Folder ---------------- #

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- Temporary Memory ---------------- #

db = {
    "documents": [],
    "active_file": None,
    "extracted_text": ""
}

# ---------------- Root ---------------- #

@app.get("/")
def root():
    return {
        "message": "Welcome to DocuMind AI Backend"
    }

# ---------------- Upload PDF ---------------- #

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = ""

    try:
        doc = fitz.open(file_path)

        for page in doc:
            text += page.get_text()

        doc.close()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF Read Error : {str(e)}"
        )

    if file.filename not in db["documents"]:
        db["documents"].append(file.filename)

    db["active_file"] = file.filename
    db["extracted_text"] = text

    return {
        "message": "PDF uploaded successfully."
    }

# ---------------- Documents ---------------- #

@app.get("/documents")
def get_documents():

    return {
        "documents": db["documents"],
        "active_file": db["active_file"]
    }

# ---------------- Select Document ---------------- #

@app.post("/select-document")
def select_document(payload: dict):

    filename = payload.get("filename")

    if filename not in db["documents"]:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    file_path = os.path.join(UPLOAD_DIR, filename)

    text = ""

    try:

        doc = fitz.open(file_path)

        for page in doc:
            text += page.get_text()

        doc.close()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    db["active_file"] = filename
    db["extracted_text"] = text

    return {
        "message": "Active document changed."
    }

# ---------------- Chat ---------------- #

@app.post("/chat")
def chat(question: str = Form(...)):

    if db["active_file"] is None:

        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF first."
        )

    answer = analyze_document(
        db["extracted_text"],
        question
    )

    return {
        "answer": answer
    }

@app.get("/test-groq")
def test_groq():
    return {
        "answer": analyze_document(
            "India is the seventh largest country in the world.",
            "Which country is mentioned?"
        )
    }

# ---------------- Test Groq ---------------- #


    