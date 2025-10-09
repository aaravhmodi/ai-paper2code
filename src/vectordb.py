import chromadb
from chromadb.config import Settings

def get_chroma_client():
    client = chromadb.Client(Settings(
        persist_directory="db/chroma_db",
        is_persistent=True
    ))
    return client

def create_or_get_collection(client, name="ai_papers"):
    try:
        return client.get_collection(name)
    except:
        return client.create_collection(name)
