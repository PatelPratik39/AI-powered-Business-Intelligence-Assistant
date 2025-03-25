# utils/pdf_utils.py

import os
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from utils.config import load_api_key

def process_pdf_folder(folder_path="../../../data/pdf_folder", persist_dir="embeddings/"):
    all_docs = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"📄 Loading: {filename}")
            loader = PyMuPDFLoader(pdf_path)
            docs = loader.load()
            all_docs.extend(docs)

    print(f"📚 Total documents loaded: {len(all_docs)}")

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(all_docs)

    embeddings = OpenAIEmbeddings(openai_api_key=load_api_key())

    # Debug: print a few chunks
    print("\n🧩 Sample chunks:")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n—– Chunk {i+1} —–\n{chunk.page_content[:500]}")
        
    # Optional: Inspect embedding vector of a sample chunk
    sample_embedding = embeddings.embed_query(chunks[0].page_content)
    print(f"\n🧠 Sample embedding vector (first 5 dims):\n{sample_embedding[:5]}")
    
    vectordb = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=persist_dir)
    vectordb.persist()

    return vectordb

