from services.query_service import generate_ans
from test_cases import test_cases

document_id = "your-uploaded-id"

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-mpnet-base-v2")

def evaluate():
    correct = 0

    for case in test_cases:
        result = generate_ans(case["query"], document_id)

        answer = result["answer"].lower()
        expected = case["expected"].lower()

        answer_emb = model.encode([answer]) 
        expected_emb = model.encode([expected])

        score = cosine_similarity(answer_emb, expected_emb)[0][0]

        if score >0.6:
            correct += 1

        print("\nQuery:", case["query"])
        print("score:", score)

    print("\nAccuracy:", correct / len(test_cases))