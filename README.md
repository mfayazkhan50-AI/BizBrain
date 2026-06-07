#  BizBrain

AI-powered business document assistant built with RAG pipeline.

## What it does
Upload your business PDFs and ask questions in plain language.
Get accurate answers with source citations instantly.

## Tech Stack
- FastAPI —> backend
- Chainlit —> chat UI
- ChromaDB —> vector database
- Groq (Llama 3) —> LLM
- HuggingFace —> embeddings
- Cohere Rerank —> reranking
- BM25 —> hybrid search

## How to run
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add `.env` file with your API keys
4. Run FastAPI: `uvicorn app.main:app --reload`
5. Run Chainlit: `chainlit run chainlit_app.py --port 8001`
