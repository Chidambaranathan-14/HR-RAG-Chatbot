import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("CRITICAL: OPENROUTER_API_KEY is missing from your environment setup!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

EMBEDDING_MODEL = "openai/text-embedding-3-small"

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    if not chunks:
        return []
    try:
        print(f"Sending batch of {len(chunks)} chunks to OpenRouter...")
        response = client.embeddings.create(
            input=chunks,
            model=EMBEDDING_MODEL
        )
        return [data.embedding for data in response.data]
    except Exception as e:
        print(f"[!] Embedding batch generation failed: {e}")
        raise e