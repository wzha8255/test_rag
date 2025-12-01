import pickle 
import numpy as np
from openai import OpenAI
from fetch_confluence import fetch_pages
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)
EMBEDDING_MODEL = "text-embedding-3-small"


# ---------------------------------------
# Chunking Function
# ---------------------------------------
def chunk_text(text, chunk_size = 500, overlap = 100):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks



def embed_text(text):
    response = client.embeddings.create(
        model = EMBEDDING_MODEL,
        input = text
    )
    return np.array(response.data[0].embedding)


def build_vectordb():
    pages = fetch_pages()
    store = {}

    for page in pages:
        page_id = page.get("id", "")
        title = page.get("title", "")
        content = page.get("content", "")

        # 1. chunk the page
        chunks = chunk_text(content)

        # 2. embed each chunk
        for idx, chunk in enumerate(chunks):
            embedding = embed_text(chunk)
            print(f"Embedded chunk {idx} of page {title}")
            chunk_id = f"{page_id}_{idx}"
            store[chunk_id] = {
                "title": title,
                "chunk": chunk,
                "embedding": embedding
            }

        print(f"Embedding complete for page {title}")

    with open("confluence_vectordb.pkl", "wb") as f:
        pickle.dump(store, f)

    print("Saving embeddings to convluence vector db file.")


if __name__ == "__main__":
    build_vectordb()