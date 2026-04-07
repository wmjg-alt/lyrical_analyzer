from src.utils.graph_utils import create_base_graph, add_topic_word_edges, add_song_topic_edges

def test_graph_construction() -> None:
    """Verify nodes and edges are properly created from topics and songs."""
    graph = create_base_graph()
    topics = {"Topic_0": ["freedom", "system"]}
    song_mapping = {"Chop_Suey": 0}
    
    add_topic_word_edges(graph, topics)
    add_song_topic_edges(graph, song_mapping)
    
    # Assert correct number of nodes (1 topic + 2 words + 1 song = 4 nodes)
    assert graph.number_of_nodes() == 4
    
    # Assert correct edges exist
    assert graph.has_edge("Topic_0", "freedom")
    assert graph.has_edge("Chop_Suey", "Topic_0")
    
    # Assert node attributes are set
    assert graph.nodes["freedom"]["type"] == "word"
    assert graph.nodes["Chop_Suey"]["type"] == "song"