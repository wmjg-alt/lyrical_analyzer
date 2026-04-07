import argparse
import json
from pathlib import Path
from src.utils.file_utils import clean_filename, create_directory
from src.utils.plot_utils import plot_topic_distribution
from src.utils.graph_utils import create_base_graph, add_topic_word_edges, add_song_topic_edges, export_network_to_dict

def parse_graph_args() -> argparse.Namespace:
    """Parse command-line arguments for graph building."""
    parser = argparse.ArgumentParser(description="Build stats and network graph.")
    parser.add_argument("--band", type=str, required=True, help="Name of the band.")
    return parser.parse_args()

def load_analysis_data(band: str) -> dict:
    """Load the analyzed JSON data for a specific band."""
    file_path = Path("data") / "export" / f"{clean_filename(band)}_analysis.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json_output(data: dict, out_path: Path) -> None:
    """Write dictionary data to a JSON file."""
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def update_band_manifest(band: str, export_dir: Path) -> None:
    """Maintain a JSON array of all processed bands for the web UI."""
    manifest_path = export_dir / "manifest.json"
    bands = set()
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            bands = set(json.load(f))
    bands.add(clean_filename(band))
    save_json_output(sorted(list(bands)), manifest_path)

def main() -> None:
    """Execute the graphing and statistical plotting pipeline."""
    args = parse_graph_args()
    data = load_analysis_data(args.band)
    safe_band = clean_filename(args.band)
    export_dir = Path("data") / "export"
    stats_dir = Path("data") / "stats"
    
    create_directory(stats_dir)
    plot_topic_distribution(data["song_mapping"], stats_dir / f"{safe_band}_topic_dist.png")
    
    graph = create_base_graph()
    add_topic_word_edges(graph, data["topics"])
    add_song_topic_edges(graph, data["song_mapping"])
    
    save_json_output(export_network_to_dict(graph), export_dir / f"{safe_band}_network.json")
    update_band_manifest(args.band, export_dir)

if __name__ == "__main__":
    main()