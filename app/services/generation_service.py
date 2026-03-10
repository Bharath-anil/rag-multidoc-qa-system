from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_name = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def generate_answer(question, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""Use the context to answer the question.

                If the question asks "what is X",
                return the sentence that defines X.
    Context:
    {context}

    Question:
    {question}

    Answer:
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