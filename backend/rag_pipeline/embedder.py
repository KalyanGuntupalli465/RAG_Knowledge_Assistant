import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EMBED_MODEL  = "nomic-embed-text-v1_5"   

class Embedder:
    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            raise ValueError("No texts provided for embedding.")

        response = requests.post(
            "https://api.groq.com/openai/v1/embeddings",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"model": EMBED_MODEL, "input": texts},
        )
        response.raise_for_status()
        data = response.json()
        return [item["embedding"] for item in data["data"]]