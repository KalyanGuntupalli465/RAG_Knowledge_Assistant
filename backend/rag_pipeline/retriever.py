from rag_pipeline.embedder import Embedder
from rag_pipeline.vector_store import query_collection

class Retriever:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.embedder = Embedder()

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Embed the query and retrieve the top_k most relevant chunks.
        Returns list of dicts with 'text', 'file_name', 'chunk_index', 'similarity_score'.
        """
        query_embedding = self.embedder.embed([query])[0]
        results = query_collection(
            collection_name=self.collection_name,
            query_embedding=query_embedding,
            n_results=top_k
        )
        return results