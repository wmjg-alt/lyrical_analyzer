from src.utils.stat_utils import build_tfidf_matrix, build_nmf_model, get_topic_words, get_song_topics

def test_tfidf_and_nmf_pipeline() -> None:
    """Verify the entire statistical pipeline extracts coherent topics."""
    sample_texts =[
        "freedom liberty revolution war",
        "freedom revolution fight",
        "love heart romance kiss",
        "heart romance feeling"
    ]
    
    # Test TF-IDF
    matrix, features = build_tfidf_matrix(sample_texts)
    assert matrix.shape[0] == 4
    
    # Test NMF
    nmf = build_nmf_model(matrix, n_topics=2)
    assert nmf.components_.shape[0] == 2
    
    # Test Topic Words Extraction
    topics = get_topic_words(nmf, features, n_words=2)
    assert "Topic_0" in topics
    assert "Topic_1" in topics
    
    # Test Document mapping
    song_topics = get_song_topics(nmf, matrix)
    assert len(song_topics) == 4
    # The first two songs should share a topic, and the last two should share the other
    assert song_topics[0] == song_topics[1]
    assert song_topics[2] == song_topics[3]
    assert song_topics[0] != song_topics[2]