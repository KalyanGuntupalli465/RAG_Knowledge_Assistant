from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self):
        self._model = None  # ← don't load at startup

    @property
    def model(self):
        if self._model is None:
            self._model = SentenceTransformer('all-MiniLM-L6-v2')  # ← loads only on first use
        return self._model

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            raise ValueError("No texts provided for embedding.")
        embeddings = self.model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embeddings.tolist()