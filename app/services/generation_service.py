from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def generate_answer(question, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
    You are a QA system.

    Use ONLY the context to answer the question.

    Context:
    {context}

    Question:
    {question}

    Give a short definition in 1-2 sentences.
    Return only the answer.
    """
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True,max_length = 1024)
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.2,
        num_beams =4,
        do_sample = False
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer