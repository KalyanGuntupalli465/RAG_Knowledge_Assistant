import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama-3.1-8b-instant"

def _get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_rag_prompt(query: str, chunks: list[dict]) -> str:
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("file_name", "unknown")
        text = chunk.get("text", "")
        context_parts.append(f"[Chunk {i} | Source: {source}]\n{text}")

    context = "\n\n---\n\n".join(context_parts)

    return f"""You are a helpful assistant that answers questions based strictly on the provided context.

CONTEXT:
{context}

---

QUESTION: {query}

INSTRUCTIONS:
- Answer using ONLY the information from the context above.
- If the context does not contain enough information, say: "I don't have enough information in the uploaded documents to answer this."
- Be concise and precise.
- Do NOT hallucinate or add outside knowledge.

ANSWER:"""

def ask_groq(query: str, chunks: list[dict]) -> str:
    client = _get_client()  # ✅ created here
    prompt = build_rag_prompt(query, chunks)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a precise document assistant. Answer only from provided context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()

def summarize_groq(chunks: list[dict]) -> str:
    client = _get_client()  # ✅ created here
    combined = "\n\n".join(chunk.get("text", "") for chunk in chunks)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a document summarizer. Produce clear, structured summaries."},
            {"role": "user", "content": f"Please provide a concise summary of the following document content:\n\n{combined}"}
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()