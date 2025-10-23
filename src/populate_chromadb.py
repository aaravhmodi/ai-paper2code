import json
import chromadb
from sentence_transformers import SentenceTransformer
import os

DB_DIR = "db/chroma_db"
METADATA_FILE = "data/metadata/arxiv.json"

def main():
    os.makedirs(DB_DIR, exist_ok=True)
    with open(METADATA_FILE, "r") as f:
        papers = json.load(f)

    print(f"📄 Loaded {len(papers)} papers")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    # Use modern ChromaDB PersistentClient API
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_or_create_collection("ai_papers")

    texts, metadatas, ids = [], [], []
    for i, paper in enumerate(papers):
        texts.append(paper["summary"])
        metadatas.append({
            "title": paper["title"],
            # ChromaDB metadata values must be primitives; store authors as a string
            "authors": ", ".join(paper["authors"]) if isinstance(paper.get("authors"), list) else paper.get("authors"),
            "pdf_url": paper["pdf_url"],
            "category": paper["primary_category"],
            "published": paper["published"]
        })
        ids.append(str(i))

    print("🧠 Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    print("💾 Inserting into ChromaDB...")
    collection.add(documents=texts, metadatas=metadatas, embeddings=embeddings, ids=ids)

    print("✅ Done! ChromaDB now contains your paper embeddings.")

if __name__ == "__main__":
    main()
