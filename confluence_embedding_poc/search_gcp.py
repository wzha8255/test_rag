import pickle
import numpy as np
from google import genai
from google.genai.types import EmbedContentConfig
from embed_pages_gcp import embed_text


client = genai.Client()
EMBEDDING_MODEL = "gemini-embedding-001"

def consine_sim(a, b):
    """ 
    calculate the cosine distance of two vectors
    
    consine similarity = A · B / (|A| X |B|)
    numpy functions: 
        - dot_product = np.dot(vector_a, vector_b)
        - magnitude = np.linalg.norm(vector_a)
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def load_embeddings():
    return pickle.load(open("confluence_vectordb.pkl", "rb"))


def search(query, top_k=5):
    vectore_store = load_embeddings()
    query_embedding = embed_text(query)

    results = []

    for chunk_id, data in vectore_store.items():
        embedding = data.get("embedding","")
        title = data.get("title", "")
        chunk = data.get("chunk", "")

        similarity_score = consine_sim(query_embedding, embedding)
        results.append((chunk_id, similarity_score, title, chunk))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    hits = search("what is adk")
    for chunk_id, score, title, chunk in hits:
        print(f"{title} ({chunk_id}) similarity score: {score}. Content: {chunk}")