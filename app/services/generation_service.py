import requests
import json
from app.core.config import settings

API_KEY = settings.OPENROUTER_API_KEY

def generate_answer(question, retrieved_chunks):
    if not retrieved_chunks:
        return "No answer found."

    context = "\n ".join(retrieved_chunks[:5])

    prompt = f"""
        You are a question answering assistant.

        Use ONLY the information from the context.

        Rules:
        - Answer the user's question directly.
        - Do NOT repeat the question.
        - Do NOT copy the context verbatim.
        - Keep the answer under 3 sentences.
        - If the answer is not found in the context, say:
        "I couldn't find this information in your uploaded documents."
        Then provide a short general answer.

        Context:
        {context}

        User Question:
        {question}

        Answer:
        """
    try:
        response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model":"openai/gpt-oss-120b:free",# "google/gemma-4-26b-a4b-it:free",
            "messages": [
                {
                "role": "user",
                "content": prompt
                }
            ],
            "max_tokens": 1024,
            "temperature": 0.1,
        })
        )

        response.raise_for_status()
        result = response.json()

        choices = result.get("choices")

        if not choices:
            return "I couldn't generate an answer right now. Please try again."

        message = choices[0].get("message", {})
        content = message.get("content")
        
        if not content:
            return (
                "I couldn't generate an answer right now. "
                "Please try again."
            )

        answer = content.strip()

        if answer.lower().startswith(question.lower()):
            answer = answer[len(question):].strip()

        if answer.startswith("?"):
            answer = answer[1:].strip()

        return answer
    except Exception as e:
        return (
            f"Error generating answer: {str(e)}"
        )