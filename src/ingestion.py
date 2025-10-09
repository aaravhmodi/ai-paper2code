import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_split_papers(data_dir="data/papers"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    all_chunks = []

    for file in os.listdir(data_dir):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(data_dir, file))
            pages = loader.load()
            chunks = splitter.split_documents(pages)
            all_chunks.extend(chunks)
            print(f"Processed {file}, {len(chunks)} chunks")

    return all_chunks
