from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def generate_answer(question, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""Use the most informative context.
    If multiple contexts mention the term, prefer explanatory sections.
    If the answer is not clearly defined, say "Not clearly defined in document."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.2
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer