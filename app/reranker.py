import cohere
import os
from dotenv import load_dotenv


load_dotenv()


co = cohere.Client(api_key=os.getenv('COHERE_API_KEY'))

def rerank(query: str, docs: list, top_n: int = 3):
    response = co.rerank(
        model='rerank-english-v3.0',
        query=query,
        documents=docs,
        top_n=top_n
    )

    reranked_docs = []
    for result in response.results:
        reranked_docs.append({
            'content': docs[result.index],
            "score": round(result.relevance_score, 3)
        })

    return reranked_docs