from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import chromadb
from rank_bm25 import BM25Okapi

embedder_fn = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

embedder_fn = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="bizbrain",
    embedding_function=embedder_fn
)

def hybrid_search(query, top_k: int = 5):
    dense_results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    dense_docs = dense_results['documents'][0]
    dense_meta = dense_results['metadatas'][0]

    all_data = collection.get()
    all_docs = all_data['documents']
    all_meta = all_data['metadatas']

    tokenized = [doc.split() for doc in all_docs]
    bm25 = BM25Okapi(tokenized)
    scores = bm25.get_scores(query.split())

    top_indices = sorted(range(len(scores)),
                         key=lambda i: scores[i],
                         reverse=True)[:top_k]
    
    bm25_docs = [all_docs[i] for i in top_indices]
    bm25_meta = [all_meta[i] for i in top_indices]

    combined = {}

    for i, doc in enumerate(dense_docs):
        combined[doc] = {"meta": dense_meta[i], "score": top_k - i}

    for i, doc in enumerate(bm25_docs):
        if doc in combined:
            combined[doc]["score"] += top_k - i
        else:
            combined[doc] = {"meta": bm25_meta[i], "score": top_k - i}

    ranked = sorted(combined.items(),
                    key=lambda x: x[1]["score"],
                    reverse=True)
    final_docs = [doc for doc, _ in ranked[:top_k]]
    final_meta = [info["meta"] for _, info in ranked[:top_k]]

    return final_docs, final_meta