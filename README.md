# 📄 DocuMind AI

An AI-powered PDF Question Answering application that allows users to upload PDF documents and ask questions based on their content. The application extracts text from PDFs and uses a local Large Language Model (LLM) through Ollama to generate accurate answers.

---

## 🚀 Features

- Upload PDF documents
- Extract text using PyMuPDF
- Ask questions related to uploaded PDFs
- AI-powered answers using Ollama (Qwen2.5:3B)
- Document history management
- Select previously uploaded documents
- Responsive React frontend
- FastAPI REST API backend

---

## 🛠️ Tech Stack

### Frontend
- React.js
- CSS
- Fetch API

### Backend
- FastAPI
- Python
- PyMuPDF

### AI Model
- Ollama
- Qwen2.5:3B

---

## 📂 Project Structure

```
DocuMind-AI/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── ai.py
│   │
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │
│   ├── package.json
│
├── uploads/
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/DocuMind-AI.git

cd DocuMind-AI
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn app.main:app --reload
```

Backend will run on

```
http://127.0.0.1:8000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend will run on

```
http://localhost:5173
```

---

## Ollama Setup

Install Ollama

Download from:

https://ollama.com

Pull the model

```bash
ollama pull qwen2.5:3b
```

Run Ollama

```bash
ollama serve
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Welcome API |
| POST | /upload | Upload PDF |
| GET | /documents | Get uploaded documents |
| POST | /select-document | Select active document |
| POST | /chat | Ask questions |
| GET | /test-groq | Test AI connection |

---

## How It Works

1. Upload a PDF.
2. Text is extracted using PyMuPDF.
3. User enters a question.
4. FastAPI sends the extracted text and question to Ollama.
5. Ollama generates the answer.
6. React displays the response.

---

## Future Improvements

- Vector Database Integration
- Semantic Search
- Multi-PDF Support
- Authentication
- Chat History
- Docker Deployment

---

## Author

**Yagsha Rafat**

GitHub:
https://github.com/yagsha31
