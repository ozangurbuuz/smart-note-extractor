from sklearn.feature_extraction.text import TfidfVectorizer


def extract_keywords(text: str, top_k: int = 7) -> list[str]:
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=2000,
    )
    matrix = vectorizer.fit_transform([text])

    scores = matrix.toarray()[0]
    terms = vectorizer.get_feature_names_out()
    ranked = sorted(zip(terms, scores), key=lambda item: item[1], reverse=True)

    return [term for term, score in ranked if score > 0][:top_k]
