import os
import uuid
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from chromadb.utils import embedding_functions

from rag_pipeline.pdf_parser import PDFParser
from rag_pipeline.chunker import Chunker
from rag_pipeline.vector_store import (
    store_chunks,
    list_collections,
    delete_collection
)
from rag_pipeline.retriever import Retriever
from rag_pipeline.llm import ask_groq, summarize_groq

load_dotenv()

app = FastAPI(title="RAG Knowledge Assistant API")

# ─────────────────────────────────────────────
# PRELOAD EMBEDDING MODEL
# Prevents first-upload timeout on Render
# ─────────────────────────────────────────────

embedding_function = embedding_functions.DefaultEmbeddingFunction()

# Warm up ONNX model
embedding_function(["hello world"])


# ─────────────────────────────────────────────
# CORS
# ─────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://rag-knowledge-assistant-sigma.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload folder
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ─────────────────────────────────────────────
# Request Models
# ─────────────────────────────────────────────

class AskRequest(BaseModel):
    collection_name: str
    query: str
    top_k: int = 5


class SummarizeRequest(BaseModel):
    collection_name: str
    top_k: int = 5


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "status": "RAG Knowledge Assistant API is running"
    }


# ─────────────────────────────────────────────
# Upload PDF
# ─────────────────────────────────────────────

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    parser = PDFParser()

    # Reduced chunk size for faster processing
    chunker = Chunker(
        chunk_size=350,
        overlap=30
    )

    file_id = str(uuid.uuid4())

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{file_id}.pdf"
    )

    # Save uploaded PDF temporarily
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # Extract text from PDF
        pages = parser.parse(file_path)

        full_text = "\n".join(pages)

        # Create chunks
        chunks = chunker.chunk(full_text)

        if not chunks:
            raise HTTPException(
                status_code=422,
                detail="Could not extract text from PDF."
            )

        # Unique collection per document
        collection_name = file_id

        # Store chunks in ChromaDB
        store_chunks(
            collection_name=collection_name,
            chunks=chunks,
            file_name=file.filename
        )

        return {
            "message": "PDF uploaded and indexed successfully.",
            "collection_name": collection_name,
            "filename": file.filename,
            "num_chunks": len(chunks)
        }

    finally:
        # Cleanup uploaded temp file
        if os.path.exists(file_path):
            os.remove(file_path)


# ─────────────────────────────────────────────
# Ask Questions
# ─────────────────────────────────────────────

@app.post("/ask")
def ask(request: AskRequest):

    try:
        retriever = Retriever(
            collection_name=request.collection_name
        )

        chunks = retriever.retrieve(
            query=request.query,
            top_k=request.top_k
        )

        if not chunks:
            return {
                "answer": "No relevant content found in the document.",
                "sources": []
            }

        answer = ask_groq(
            query=request.query,
            chunks=chunks
        )

        sources = [
            {
                "text": c["text"][:200] + "...",
                "similarity_score": c["similarity_score"]
            }
            for c in chunks
        ]

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ─────────────────────────────────────────────
# Summarize Document
# ─────────────────────────────────────────────

@app.post("/summarize")
def summarize(request: SummarizeRequest):

    try:
        retriever = Retriever(
            collection_name=request.collection_name
        )

        chunks = retriever.retrieve(
            query="main topics overview summary",
            top_k=request.top_k
        )

        if not chunks:
            return {
                "summary": "No content found in the document."
            }

        summary = summarize_groq(chunks=chunks)

        return {
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ─────────────────────────────────────────────
# List Documents
# ─────────────────────────────────────────────

@app.get("/documents")
def list_documents():

    try:
        collections = list_collections()

        return {
            "collections": collections
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ─────────────────────────────────────────────
# Delete Document
# ─────────────────────────────────────────────

@app.delete("/documents/{collection_name}")
def delete_document(collection_name: str):

    try:
        delete_collection(collection_name)

        return {
            "message": f"Collection '{collection_name}' deleted successfully."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )