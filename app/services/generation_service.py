from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

tokenizer = None
model = None

tokenizer = None
model = None

def get_model():
    global tokenizer, model

    if model is None or tokenizer is None:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

        model_name = "google/flan-t5-small"

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    return tokenizer, model


def generate_answer(question, retrieved_chunks):
    if not retrieved_chunks:
        return "No answer found."

    tokenizer, model = get_model()

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
    Answer the question using the context.

    Context:
    {context}

    Question:
    {question}

    Answer in 1-2 sentences.
    """

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

    outputs = model.generate(
        **inputs,
        max_new_tokens=100
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)