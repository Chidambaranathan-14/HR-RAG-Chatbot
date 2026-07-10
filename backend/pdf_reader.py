import os
from typing import List
from pypdf import PdfReader # This is the external library import

def read_pdf(pdf_path: str) -> List[str]:
    """
    Reads a target PDF file path and extracts textual strings from its pages.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"CRITICAL: The file path '{pdf_path}' does not exist.")
        
    reader = PdfReader(pdf_path)
    pages = [page.extract_text() for page in reader.pages if page.extract_text()]
    return pages