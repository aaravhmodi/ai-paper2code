# src/retriever.py
from sentence_transformers import SentenceTransformer
import chromadb

# --- Load the same model used for embeddings ---
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# --- Connect to your existing persistent ChromaDB ---
client = chromadb.PersistentClient(path="db/chroma_db")
collection = client.get_or_create_collection("ai_papers")

# --- Function to query documents ---
def query_docs(query, n=5):
    q_emb = embedder.encode([query])
    res = collection.query(query_embeddings=q_emb, n_results=n)

    docs = res["documents"][0]
    metas = res["metadatas"][0]

    formatted = []
    for doc, meta in zip(docs, metas):
        # authors may be stored as a string or a list; normalize for display
        authors = meta.get('authors')
        if isinstance(authors, list):
            authors_display = ', '.join(authors[:3])
        else:
            authors_display = str(authors) if authors else 'N/A'

        formatted.append(
            f"📘 {meta.get('title', 'untitled')} ({meta.get('category', 'unknown')})\n"
            f"Authors: {authors_display}\n"
            f"Abstract: {doc[:400]}...\n"
        )

    return "\n\n".join(formatted)

# --- Optional helper if you ever want to add new docs dynamically ---
def add_documents(chunks):
    texts = [c.page_content for c in chunks]
    embeddings = embedder.encode(texts)
    ids = [str(i) for i in range(len(texts))]

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids
    )
    print(f"✅ Added {len(texts)} documents to ChromaDB")

if __name__ == "__main__":
    print(query_docs("implement diffusion model in PyTorch"))
