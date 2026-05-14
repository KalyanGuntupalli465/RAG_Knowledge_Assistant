import chromadb
from chromadb.config import Settings
import os

# Persistent storage path
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

def get_chroma_client():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client


def get_or_create_collection(collection_name: str):
    """Getting an existing collection or create a new one."""
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}  # cosine similarity
    )
    return collection


def store_chunks(
    collection_name: str,
    chunks: list[dict],
    embeddings: list[list[float]],
    file_name: str
):
    """
    Storing text chunks + embeddings into ChromaDB.
    """
    collection = get_or_create_collection(collection_name)
    ids = []
    documents = []
    metadatas = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        chunk_id = f"{file_name}_chunk_{chunk['chunk_index']}"
        ids.append(chunk_id)
        documents.append(chunk['text'])
        metadatas.append({
            "file_name": file_name,
            "chunk_index": chunk['chunk_index'],
            "word_count": chunk['word_count']  
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"✅ Stored {len(ids)} chunks from '{file_name}' into collection '{collection_name}'")
    return len(ids)


def query_collection(
    collection_name: str,
    query_embedding: list[float],
    n_results: int = 5
) -> list[dict]:
 
    collection = get_or_create_collection(collection_name)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    retrieved = []
    for doc, meta, dist in zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    ):
        retrieved.append({
            "text": doc,
            "file_name": meta['file_name'],
            "chunk_index": meta['chunk_index'],
            "similarity_score": round(1 - dist, 4)  # convert distance to similarity
        })

    return retrieved


def delete_collection(collection_name: str):
    """Deleting a collection """
    client = get_chroma_client()
    client.delete_collection(name=collection_name)
    print(f" Deleted collection: {collection_name}")


def list_collections() -> list[str]:
    """Listing all existing collections."""
    client = get_chroma_client()
    return [col.name for col in client.list_collections()]