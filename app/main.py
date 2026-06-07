from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os
from ingest import ingest_pdf
from retriever import hybrid_search
from reranker import rerank
from generator import generate_answer

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f'../uploads/{file.filename}'
    os.makedirs("../uploads", exist_ok=True)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    ingest_pdf(file_path)
    return {'message': f"{file.filename} uploaded and ingested successfuly"}

@app.post("/ask")
async def ask_question(request: QueryRequest):
    docs, meta = hybrid_search(request.question)
    reranked = rerank(request.question, docs, top_n=3)
    answer = generate_answer(request.question, reranked)
    
    sources = list(set([
        m.get("source", "Unknown") for m in meta[:3]
    ]))
    
    return {
        "answer": answer,
        "sources": sources
    }

@app.get('/')
async def root():
    return {'message': 'BizBrain API is running'}