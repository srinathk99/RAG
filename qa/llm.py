import ollama


def ask_llm(context_chunks, question):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a document understanding assistant.
Answer ONLY using the context below.

Context:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
