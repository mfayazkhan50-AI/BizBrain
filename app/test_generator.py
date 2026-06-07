from retriever import hybrid_search
from reranker import rerank
from generator import generate_answer

query = "what are your skills?"

docs, meta = hybrid_search(query)
print("Docs found:", len(docs))

reranked = rerank(query, docs, top_n=3)
print("Reranked:", len(reranked))
print("First doc:", reranked[0]['content'][:100])

answer = generate_answer(query, reranked)

print("\n=== ANSWER ===")
print(answer)