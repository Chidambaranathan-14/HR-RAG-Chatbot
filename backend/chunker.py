from typing import List, Tuple



def chunk_pages(pages: list[str], chunk_size: int = 700 , chunk_overlap: int = 100 ) -> List[str]:

    chunks:list[str]=[]



    full_text = " ".join(pages)

    text_length = len(full_text)



    if text_length == 0:

        return chunks

   

    start = 0

    while start < text_length:



        end = min(start + chunk_size, text_length)



        chunk = full_text[start:end]

       

        chunks.append(chunk)

       

        if end == text_length:

            break



        start =end - chunk_overlap

        print("starting new chunk at index:", start)



    return chunks

