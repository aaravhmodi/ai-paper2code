from sentence_transformers import SentenceTransformer

def get_embedder():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

def embed_texts(embedder, texts):
    return embedder.encode(texts, show_progress_bar=True)
