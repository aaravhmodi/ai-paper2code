from src.embeddings import get_embedder
from src.vectordb import get_chroma_client, create_or_get_collection

embedder = get_embedder()
client = get_chroma_client()
collection = create_or_get_collection(client)

def add_documents(chunks):
    texts = [c.page_content for c in chunks]
    embeddings = embedder.encode(texts)
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=[str(i) for i in range(len(texts))]
    )
    print("Documents added to ChromaDB.")

def query_docs(query, n=5):
    q_emb = embedder.encode([query])
    res = collection.query(query_embeddings=q_emb, n_results=n)
    return "\n\n".join(res["documents"][0])
