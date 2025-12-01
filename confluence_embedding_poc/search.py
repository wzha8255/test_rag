import pickle
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key = api_key)
EMBEDDING_MODEL = "text-embedding-3-small"

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


def embedding_query(query):
    response = client.embeddings.create(
        model = EMBEDDING_MODEL,
        input = query
    )
    return np.array(response.data[0].embedding)


def search(query, top_k=5):
    vectore_store = load_embeddings()
    query_embedding = embedding_query(query)

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