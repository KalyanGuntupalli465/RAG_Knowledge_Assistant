class Chunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[dict]:
        """
        Split text into overlapping word-based chunks.
        Returns list of dicts with 'chunk_index', 'text', 'word_count'.
        """
        words = text.split()
        chunks = []
        start = 0
        chunk_index = 0

        while start < len(words):
            end = start + self.chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunks.append({
                "chunk_index": chunk_index,
                "text": chunk_text,
                "word_count": len(chunk_words),
                "start_word": start,
                "end_word": end
            })

            chunk_index += 1
            start += self.chunk_size - self.overlap

        return chunks