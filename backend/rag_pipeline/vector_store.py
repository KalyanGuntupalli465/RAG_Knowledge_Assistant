import chromadb
import os

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)

def get_or_create_collection(collection_name: str):
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
        embedding_function=None
    )

def store_chunks(
    collection_name: str,
    chunks: list[dict],
    embeddings: list[list[float]],
    file_name: str
):
    collection = get_or_create_collection(collection_name)
    ids, documents, metadatas = [], [], []

    for chunk, embedding in zip(chunks, embeddings):
        ids.append(f"{file_name}_chunk_{chunk['chunk_index']}")
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
            "similarity_score": round(1 - dist, 4)
        })
    return retrieved

def delete_collection(collection_name: str):
    get_chroma_client().delete_collection(name=collection_name)

def list_collections() -> list[str]:
    return [col.name for col in get_chroma_client().list_collections()]