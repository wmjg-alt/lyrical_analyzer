import networkx as nx

def create_base_graph() -> nx.Graph:
    """Initialize an empty undirected network graph."""
    return nx.Graph()

def add_topic_word_edges(graph: nx.Graph, topics: dict) -> None:
    """Add nodes and edges connecting topics to their top words."""
    for topic, words in topics.items():
        graph.add_node(topic, type="topic", group=topic)
        for word in words:
            graph.add_node(word, type="word", group=topic)
            graph.add_edge(topic, word, weight=2)

def add_song_topic_edges(graph: nx.Graph, song_mapping: dict) -> None:
    """Add nodes and edges connecting songs to their primary topics."""
    for song, topic_id in song_mapping.items():
        topic_name = f"Topic_{topic_id}"
        graph.add_node(song, type="song", group=topic_name)
        graph.add_edge(song, topic_name, weight=1)

def export_network_to_dict(graph: nx.Graph) -> dict:
    """Export graph structure to a D3-compatible node-link dictionary."""
    return nx.node_link_data(graph, edges="links")