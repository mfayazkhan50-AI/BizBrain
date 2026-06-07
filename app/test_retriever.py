from retriever import hybrid_search

query = "what are your skills?"
docs, meta = hybrid_search(query)

for i, (doc, m) in enumerate(zip(docs, meta)):
    print(f"\n--- Result {i+1} ---")
    print(f"Source: {m['source']}")
    print(f"Content: {doc[:200]}")