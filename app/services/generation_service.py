import requests
import json
from app.core.config import settings

API_KEY = settings.OPENROUTER_API_KEY

def generate_answer(question, retrieved_chunks):
    if not retrieved_chunks:
        return "No answer found."

    context = retrieved_chunks[0]

    prompt = f"""
        Answer the question in ONE short sentence.

        Only return the final answer.
        Do NOT include explanations.
        Do NOT repeat context.

        Context:
        {context}

        Question:
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
            "reasoning": {"enabled": True},
            "max_tokens": 60,
            "temperature": 0.1,
        })
        )


        result = response.json()

        choices = result.get("choices")

        if not choices:
            return f"API Error: {result}"

        message = choices[0].get("message", {})
        content = message.get("content")

        if not content:
            return f"Empty response: {result}"

        answer = content.strip()

        # keep only first sentence
        if "." in answer:
            answer = answer.split(".")[0] + "."

        return answer

    except Exception as e:
        return f"Error generating answer: {str(e)}"