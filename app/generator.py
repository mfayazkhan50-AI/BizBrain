import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def generate_answer(query: str, reranked_docs: list):
    context = ""
    for i, item in enumerate(reranked_docs):
        context += f"\n[Source {i+1}]\n{item['content']}\n"

    prompt = f"""You are a helpful business assistant.
Use the following context to answer the question.
If the answer is in the context, answer it clearly.
Always mention which source you used.

Context:
{context}

Question: {query}

Answer:"""

    print("DEBUG context length:", len(context))  # debug line

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer based on the provided context only."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content