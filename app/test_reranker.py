from retriever import hybrid_search
from reranker import rerank

query = "what are your skills?"

docs, meta = hybrid_search(query)
reranked = rerank(query, docs, top_n=3)

for i, item in enumerate(reranked):
    print(f"\n--- Result {i+1} ---")
    print(f"Score: {item['score']}")
    print(f"Content: {item['content'][:200]}")

    