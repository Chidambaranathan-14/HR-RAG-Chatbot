from typing import List
# FIX: Import the function 'read_pdf', NOT the class 'PdfReader'
from pdf_reader import read_pdf 
from chunker import chunk_pages
from embedder import embed_chunks
from vector_store import store_in_pinecone

PDF_PATH = r"D:\python\Rag\backend\resources\New_HR_Policies_20_.pdf"

# The rest of your data_processor.py code remains exactly the same...

def run_pipeline() -> None:
    """
    Executes the ingestion pipeline: Read PDF -> Chunk Text -> Generate Vectors -> Upsert to DB.
    """
    print(f"--- [STARTING INGESTION PIPELINE] Processing: {PDF_PATH} ---")
    
    # Step 1: Read PDF Text Pages
    pages = read_pdf(PDF_PATH)
    print(f"[1/4] Successfully read PDF file. Total pages parsed: {len(pages)}")

    # Step 2: Build Text Chunks with Overlaps
    chunks = chunk_pages(pages, chunk_size=700, chunk_overlap=100)
    print(f"[2/4] Completed chunk division logic. Generated {len(chunks)} structural chunks.")

    # Step 3: Embed Text Strings in Batch Calls
    embeddings = embed_chunks(chunks)
    print(f"[3/4] Successfully received embeddings back from OpenRouter.")

    # Step 4: Securely Upsert Vectors into Pinecone Database Index
    print("[4/4] Sending batch payload packets to Pinecone...")
    store_in_pinecone(chunks, embeddings, namespace="")
    
    print("\n--- [INGESTION COMPLETE] Your RAG knowledge base is active! ---\n")

if __name__ == "__main__":
    run_pipeline()