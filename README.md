# 🧠 RAG Knowledge Assistant

A full-stack AI-powered document assistant that allows users to upload PDFs, ask context-aware questions, and generate intelligent summaries using a Retrieval-Augmented Generation (RAG) pipeline.

An AI-powered Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents, ask questions, and generate intelligent summaries using Large Language Models.

Built with FastAPI, ChromaDB, ONNX embeddings, Groq LLM, React, and Vite.

---

# 🚀 Live Demo

### Frontend

🔗 [https://rag-knowledge-assistant-sigma.vercel.app/](https://rag-knowledge-assistant-sigma.vercel.app/)

### Backend API

🔗 [https://rag-knowledge-assistant-zpwr.onrender.com/docs](https://rag-knowledge-assistant-zpwr.onrender.com/docs)

---

# 📌 Features

* 📄 Upload and index PDF documents instantly

* 💬 Chat with uploaded documents using AI-powered semantic retrieval

* ✨ Generate concise document summaries

* 📚 Support for multiple uploaded documents

* 🗑️ Delete and manage indexed document collections

* ⚡ Fast inference using Groq LLM

* 🧠 Semantic vector search using ChromaDB

* 🌐 Fully deployed full-stack architecture using Vercel + Render

* 📱 Responsive and modern user interface

* 📄 Upload PDF documents

* ✂️ Intelligent text chunking

* 🔍 Semantic search using vector embeddings

* 🤖 Ask questions from uploaded PDFs

* ✨ AI-generated document summaries

* ⚡ Fast inference using Groq LLM

* 🧠 ChromaDB vector database integration

* 🌐 Full-stack deployment using Vercel + Render

* 📱 Responsive and modern UI

---

# 🛠️ Tech Stack

## Frontend

* React.js
* Vite
* Axios
* Tailwind CSS

## Backend

* FastAPI
* Python
* ChromaDB
* ONNX Runtime
* pdfplumber
* Groq API

## Deployment

* Vercel (Frontend)
* Render (Backend)

---

# 🧩 System Architecture

```text
Frontend (React + Vite)
        ↓
Backend API (FastAPI)
        ↓
PDF Parsing + Chunking
        ↓
ChromaDB Vector Store
        ↓
Semantic Retrieval
        ↓
Groq LLM Response Generation
```

---

# 🏗️ Architecture Overview

```text
User Uploads PDF
        ↓
PDF Parsing (pdfplumber)
        ↓
Text Chunking
        ↓
ChromaDB + ONNX Embeddings
        ↓
Semantic Retrieval
        ↓
Groq LLM
        ↓
AI Response / Summary
```

---

# 📂 Project Structure

```text
RAG-Knowledge-Assistant/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── runtime.txt
│   ├── chroma_db/
│   ├── uploaded_pdfs/
│   └── rag_pipeline/
│       ├── pdf_parser.py
│       ├── chunker.py
│       ├── retriever.py
│       ├── vector_store.py
│       └── llm.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api/
│   │   ├── components/
│   │   └── pages/
│   └── vite.config.js
│
└── README.md
```

---

# ⚙️ How the RAG Pipeline Works

1. User uploads a PDF document
2. PDF text is extracted using pdfplumber
3. Text is split into overlapping chunks
4. ChromaDB generates vector embeddings
5. Embeddings are stored in the vector database
6. User asks a question
7. Most relevant chunks are retrieved semantically
8. Retrieved context is sent to Groq LLM
9. AI generates context-aware response

```text
RAG-Knowledge-Assistant/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── rag_pipeline/
│   │   ├── chunker.py
│   │   ├── pdf_parser.py
│   │   ├── retriever.py
│   │   ├── vector_store.py
│   │   └── llm.py
│   │
│   └── uploaded_pdfs/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── services/
│
└── README.md
```

---

# ⚙️ Backend Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/rag-knowledge-assistant.git
cd rag-knowledge-assistant/backend
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Create .env File

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 5️⃣ Run Backend

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# 💻 Frontend Setup

## 1️⃣ Navigate to Frontend

```bash
cd ../frontend
```

---

## 2️⃣ Install Dependencies

```bash
npm install
```

---

## 3️⃣ Configure Environment Variable

Create `.env`:

```env
VITE_API_URL=http://127.0.0.1:8000
```

---

## 4️⃣ Run Frontend

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

# 🌐 Deployment

## Frontend Deployment (Vercel)

Environment Variable:

```env
VITE_API_URL=https://rag-knowledge-assistant-zpwr.onrender.com
```

---

## Backend Deployment (Render)

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### runtime.txt

```text
python-3.11.9
```

---

# 🔍 API Endpoints

| Method | Endpoint                       | Description                 |
| ------ | ------------------------------ | --------------------------- |
| GET    | `/`                            | Health check                |
| POST   | `/upload`                      | Upload and index PDF        |
| POST   | `/ask`                         | Ask questions from document |
| POST   | `/summarize`                   | Generate AI summary         |
| GET    | `/documents`                   | List uploaded collections   |
| DELETE | `/documents/{collection_name}` | Delete collection           |

---

# 🧠 How Retrieval-Augmented Generation (RAG) Works

RAG combines:

* Information Retrieval
* Vector Search
* Large Language Models

Workflow:

1. PDF text is extracted
2. Text is split into chunks
3. Chunks are converted into vector embeddings
4. ChromaDB stores embeddings
5. User query is embedded
6. Most relevant chunks are retrieved
7. Retrieved context is sent to Groq LLM
8. AI generates context-aware response

---

# ⚡ Performance Optimizations

* Lightweight ONNX embedding runtime
* ChromaDB semantic retrieval
* Optimized chunk sizes for faster indexing
* Fast Groq inference
* Reduced deployment memory usage for Render free tier

---

# 📸 Screenshots

## Upload & Chat Interface

(Add screenshot here)

## AI Summary Feature

(Add screenshot here)

---

# 🎯 Future Improvements

* Multi-document querying
* Chat history persistence
* Authentication system
* Streaming responses
* Drag & drop multiple PDFs
* Support for DOCX and TXT files
* Citation highlighting

---

# 👨‍💻 Author

Kalyan Guntupalli

* AI/ML Enthusiast
* Data Science Graduate Student
* Passionate about Generative AI and Full-Stack AI Applications

---

# 📜 License

This project is for educational and portfolio purposes.

---

# ⭐ Acknowledgements

* FastAPI
* ChromaDB
* Groq
* React
* Vercel
* Render
* ONNX Runtime
