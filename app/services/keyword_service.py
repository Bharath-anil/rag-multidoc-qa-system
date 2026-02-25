from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_keyword_scores(question, chunks):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(chunks + [question])

    chunk_vectors = tfidf_matrix[:-1] # type: ignore
    question_vector = tfidf_matrix[-1] # type: ignore

    scores = cosine_similarity(question_vector, chunk_vectors)[0]

    return scores