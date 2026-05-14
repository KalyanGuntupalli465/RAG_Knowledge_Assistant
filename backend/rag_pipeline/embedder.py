from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a list of text strings.
        Returns list of float vectors.
        """
        if not texts:
            raise ValueError("No texts provided for embedding.")

        embeddings = self.model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embeddings.tolist()