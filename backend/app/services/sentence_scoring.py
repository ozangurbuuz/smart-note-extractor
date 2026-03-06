import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def score_sentences(sentences: list[str]) -> list[tuple[int, str, float]]:
    if len(sentences) == 1:
        return [(0, sentences[0], 1.0)]

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(sentences)

    tfidf_scores = matrix.sum(axis=1).A1
    position_bonus = np.linspace(0.15, 0.0, len(sentences))
    combined_scores = tfidf_scores + position_bonus

    max_score = float(np.max(combined_scores)) if len(combined_scores) else 1.0
    normalized = combined_scores / max_score if max_score else combined_scores

    return [(index, sentence, float(normalized[index])) for index, sentence in enumerate(sentences)]
