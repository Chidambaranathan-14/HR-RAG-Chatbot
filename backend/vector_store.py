import os
from typing import List, Any
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv(override=True)

# Initialize client safely
pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pinecone_client.Index(os.getenv("PINECONE_INDEX_NAME"))

def store_in_pinecone(chunks: List[str], embeddings: List[List[float]], namespace: str = "") -> None:
    vector_to_upsert = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vector_to_upsert.append({
            "id": f"chunk_{i}",
            "values": embedding,
            "metadata": {
                "text": chunk,
                "chunk_index": i,
                "source": "New_HR_Policies_2026.pdf",
                "version": 2,
                "status": "active"  # <-- Ithu thaan mukkiyam
            }
        })

    # FIX 1: Lower batch size from 20 to 10 to keep network request sizes lightweight
    batch_size = 10  
    print(f"Total chunks to upsert to Pinecone: {len(vector_to_upsert)}")

    for i in range(0, len(vector_to_upsert), batch_size):
        batch = vector_to_upsert[i : i + batch_size]
        print(f"Uploading batch: chunks index {i} to {i + len(batch)}...")
        
        try:
            # FIX 2: Added explicit timeout=60 to give your network ample time to upload high-dim vectors
            index.upsert(vectors=batch, namespace=namespace, timeout=60)
        except Exception as e:
            print(f"\n[!] Failed to upload batch at index {i}. Error: {e}")
            raise e
        
    print("Successfully uploaded all embeddings to Pinecone!")

def query_pinecone(query_embedding: List[float], top_k: int = 3, namespace: str = "") -> List[Any]:
    response = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True,
    # 👇 INTHA FILTER-AH ADD PANNUNGA
    filter={
        "status": {"$eq": "active"}  # "active"-ah irukura puthu data mattum thaan varum
    }
)
    return response.matches