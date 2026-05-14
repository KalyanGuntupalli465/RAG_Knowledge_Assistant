from rag_pipeline.vector_store import query_collection


class Retriever:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Retrieve the top_k most relevant chunks.
        """

        results = query_collection(
            collection_name=self.collection_name,
            query_text=query,
            n_results=top_k
        )

        return results