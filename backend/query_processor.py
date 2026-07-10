from typing import List
from embedder import embed_chunks
from vector_store import query_pinecone
from llm import generate_response

def process_user_query(query: str, namespace: str = "") -> str:
    print(f"\nProcessing user query: '{query}' in namespace: '{namespace}'")
    
    # 1. Generate query vector
    query_embeddings = embed_chunks([query])
    if not query_embeddings:
        return "Failed to process query vector."
    query_embedding = query_embeddings[0]
    
    # 2. Query Pinecone with matching namespace parameter
    matches = query_pinecone(query_embedding, top_k=3, namespace=namespace)
    
    if not matches:
        print("No matching policies found.")
        return "I could not find any relevant HR policy matches inside the system data."
    
    # 3. Compile context documents
    contexts = []
    for match in matches:
        metadata = getattr(match, "metadata", {})
        text = metadata.get("text", "")
        score = getattr(match, "score", 0.0)
        print(f"Retrieved chunk (score: {score:.4f}): {text[:100]}...")
        contexts.append(text)
        
    context_str = "\n---\n".join(contexts)
    
    # 4. Generate Answer via Gemini
    return generate_response(query, context_str)

if __name__ == "__main__":
    user_query = input('Enter your HR policy question: ')
    process_user_query(user_query)