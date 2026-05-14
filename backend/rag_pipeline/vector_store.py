import chromadb
import os
import uuid
import requests

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)

def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings via Groq API — no local model, no memory cost."""
    response = requests.post(
        "https://api.groq.com/openai/v1/embeddings",
        headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"},
        json={"model": "nomic-embed-text-v1_5", "input": texts},
    )
    response.raise_for_status()
    return [item["embedding"] for item in response.json()["data"]]

def get_or_create_collection(collection_name: str):
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
        embedding_function=None   # ← critical: prevents ChromaDB loading sentence-transformers
    )

def store_chunks(collection_name: str, chunks: list[dict], file_name: str):
    collection = get_or_create_collection(collection_name)

    texts = [chunk["text"] for chunk in chunks]
    embeddings = get_embeddings(texts)   # ← we embed via Groq, not ChromaDB

    ids = []
    metadatas = []
    for chunk in chunks:
        ids.append(str(uuid.uuid4()))
        metadatas.append({
            "file_name": file_name,
            "chunk_index": chunk["chunk_index"],
            "word_count": chunk["word_count"]
        })

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,   # ← pass pre-built embeddings, ChromaDB stores them as-is
        metadatas=metadatas
    )
    return len(ids)

def query_collection(collection_name: str, query_text: str, n_results: int = 5) -> list[dict]:
    collection = get_or_create_collection(collection_name)

    query_embedding = get_embeddings([query_text])[0]   # ← embed the query via Groq too

    results = collection.query(
        query_embeddings=[query_embedding],   # ← pass embedding directly, not query_texts
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