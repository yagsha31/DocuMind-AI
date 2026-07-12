import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [uploadMessage, setUploadMessage] = useState("")
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [loading, setLoading] = useState(false)
  const [documents, setDocuments] = useState([])
  const [activeFile, setActiveFile] = useState("")

  // LIVE RENDER BACKEND URL
  const BACKEND_URL = "https://documind-backend-hzp4.onrender.com";

  // API se uploaded documents ki list fetch karne ka function
  const fetchDocuments = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/documents`)
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`)
      }
      const data = await response.json()
      if (data) {
        setDocuments(data.documents || [])
        setActiveFile(data.active_file || "")
      }
    } catch (error) {
      console.error("Error fetching documents:", error)
    }
  }

  // React 19 safe mount fetch
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchDocuments()
    }, 0)
    return () => clearTimeout(timer)
  }, [])

  // File select handler
  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  // PDF Upload handler
  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.")
      return
    }

    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch(`${BACKEND_URL}/upload`, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`)
      }

      const data = await response.json()
      setUploadMessage(data.message)
      fetchDocuments() 

    } catch (error) {
      console.error(error)
      if (error instanceof Error) {
        setUploadMessage(`Error: ${error.message}`)
      }
    }
  }

  // Dropdown change handler
  const handleDropdownChange = async (e) => {
    const selectedDoc = e.target.value
    if (!selectedDoc) return

    try {
      const response = await fetch(`${BACKEND_URL}/select-document`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ filename: selectedDoc }),
      })

      if (response.ok) {
        const data = await response.json()
        setActiveFile(selectedDoc)
        alert(data.message)
      }
    } catch (error) {
      console.error("Error selecting document:", error)
      alert("Failed to select document")
    }
  }

  // AI query handler
  const handleAsk = async () => {
    if (!question) {
      alert("Please enter a question.")
      return
    }

    setLoading(true)
    const formData = new FormData()
    formData.append("question", question)

    try {
      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`)
      }

      const data = await response.json()
      setAnswer(data.answer)
      setLoading(false)

    } catch (error) {
      console.error(error)
      setLoading(false)
      if (error instanceof Error) {
        setAnswer(`Error: ${error.message}`)
      }
    }
  }

  return (
    <div className="container">
      <h1>📄 DocuMind AI</h1>

      {/* Upload Section */}
      <div className="upload-box">
        <input type="file" id="file-upload" style={{ display: "none" }} onChange={handleFileChange} />
        <label htmlFor="file-upload" className="file-label">
          {file ? `📁 ${file.name}` : "➕ Click to select PDF"}
        </label>
        
        {file && (
          <button onClick={handleUpload}>Upload selected file</button>
        )}
        {uploadMessage && <p style={{ color: "#2563eb", fontSize: "14px", marginTop: "10px" }}>{uploadMessage}</p>}
      </div>

      {/* History Dropdown Section */}
      <div className="history-box">
        <label htmlFor="doc-select"><b>Select from history:</b></label>
        <select id="doc-select" className="doc-select" value={activeFile} onChange={handleDropdownChange}>
          <option value="">-- Choose a PDF --</option>
          {documents.map((doc, index) => (
            <option key={index} value={doc}>{doc}</option>
          ))}
        </select>
        {activeFile && <p className="status-active">🟢 Active Document: {activeFile}</p>}
      </div>

      <hr className="divider" />

      {/* Chat Input Section */}
      <div className="chat-section">
        <h2>Ask a Question</h2>
        <textarea
          value={question}
          onChange={(e) => {
            setQuestion(e.target.value)
            e.target.style.height = "auto"
            e.target.style.height = e.target.scrollHeight + "px"
          }}
          placeholder="Ask anything about the selected PDF..."
          rows={2}
        />
        <button className="btn-block" onClick={handleAsk} disabled={loading}>
          {loading ? "⚡ Thinking..." : "Ask AI"}
        </button>
      </div>

      {/* Answer Box */}
      {answer && (
        <div className="answer-container">
          <h3>💡 Answer</h3>
          <div className="answer-box">{answer}</div>
        </div>
      )}
    </div>
  )
}

export default App