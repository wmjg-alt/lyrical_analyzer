from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

def build_tfidf_matrix(texts: list[str], max_features: int = 1000):
    """Vectorize text list into a TF-IDF matrix and return feature names."""
    vectorizer = TfidfVectorizer(max_features=max_features)
    matrix = vectorizer.fit_transform(texts)
    return matrix, vectorizer.get_feature_names_out()

def build_nmf_model(tfidf_matrix, n_topics: int = 5) -> NMF:
    """Fit and return an NMF topic model from a TF-IDF matrix."""
    nmf = NMF(n_components=n_topics, random_state=42)
    nmf.fit(tfidf_matrix)
    return nmf

def get_topic_words(nmf_model: NMF, feature_names: list[str], n_words: int = 10) -> dict:
    """Extract the top n words for each topic from the NMF model."""
    topics = {}
    for i, topic in enumerate(nmf_model.components_):
        top_indices = topic.argsort()[:-n_words - 1:-1]
        topics[f"Topic_{i}"] =[feature_names[idx] for idx in top_indices]
    return topics

def get_song_topics(nmf_model: NMF, tfidf_matrix) -> list[int]:
    """Return the dominant topic index for each document in the matrix."""
    topic_weights = nmf_model.transform(tfidf_matrix)
    return topic_weights.argmax(axis=1).tolist()