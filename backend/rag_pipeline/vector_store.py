import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
import os
import uuid

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

# Single shared instance — loaded once, reused every call
_embedding_fn = None

def get_embedding_fn():
    global _embedding_fn
    if _embedding_fn is None:
        _embedding_fn = DefaultEmbeddingFunction()
    return _embedding_fn

def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)

def get_or_create_collection(collection_name: str):
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
        embedding_function=get_embedding_fn()
    )

def store_chunks(collection_name: str, chunks: list[dict], file_name: str):
    collection = get_or_create_collection(collection_name)

    ids = []
    documents = []
    metadatas = []
    for chunk in chunks:
        ids.append(str(uuid.uuid4()))
        documents.append(chunk["text"])
        metadatas.append({
            "file_name": file_name,
            "chunk_index": chunk["chunk_index"],
            "word_count": chunk["word_count"]
        })

    # ChromaDB uses the ONNX embedder (not PyTorch) — safe on free tier
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    return len(ids)

def query_collection(collection_name: str, query_text: str, n_results: int = 5) -> list[dict]:
    collection = get_or_create_collection(collection_name)

    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    retrieved = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        retrieved.append({
            "text": doc,
            "file_name": meta["file_name"],
            "chunk_index": meta["chunk_index"],
            "similarity_score": round(1 - dist, 4)
        })
    return retrieved

def delete_collection(collection_name: str):
    get_chroma_client().delete_collection(name=collection_name)

def list_collections() -> list[str]:
    return [col.name for col in get_chroma_client().list_collections()]