import os
import uuid
from pypdf import PdfReader
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import chromadb


load_dotenv()

# embedding model
embedder_fn = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# chromadb client
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="bizbrain",
    embedding_function=embedder_fn
)


def ingest_pdf(file_path: str):
    file_name = os.path.basename(file_path)
    
    # duplicate check
    existing = collection.get(where={"source": file_name})
    if existing["documents"]:
        print(f"Already ingested: {file_name}")
        return

    reader = PdfReader(file_path)
    full_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text += f"\n[Page {i+1}]\n{text}"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(full_text)

    ids = [f"{file_name}_chunk_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=[{"source": file_name} for _ in chunks]
    )

    print(f"Done - {len(chunks)} chunks saved to {file_name}")