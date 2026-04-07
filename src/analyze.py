import argparse
import pandas as pd
import json
from pathlib import Path
from src.utils.file_utils import clean_filename, create_directory
from src.utils.stat_utils import build_tfidf_matrix, build_nmf_model, get_topic_words, get_song_topics

def parse_analyze_args() -> argparse.Namespace:
    """Parse command-line arguments for analysis."""
    parser = argparse.ArgumentParser(description="Analyze processed lyrics.")
    parser.add_argument("--band", type=str, required=True, help="Name of the band.")
    parser.add_argument("--topics", type=int, default=5, help="Number of topics to extract.")
    return parser.parse_args()

def load_processed_data(band: str) -> pd.DataFrame:
    """Load the processed JSON data for a specific band."""
    file_path = Path("data") / "processed" / f"{clean_filename(band)}_processed.json"
    return pd.read_json(file_path)

def save_analysis(data: dict, band: str) -> None:
    """Save the extracted topics and song mappings to JSON."""
    out_dir = Path("data") / "export"
    create_directory(out_dir)
    safe_band = clean_filename(band)
    with open(out_dir / f"{safe_band}_analysis.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main() -> None:
    """Execute the statistical analysis pipeline."""
    args = parse_analyze_args()
    df = load_processed_data(args.band)
    
    # Filter out empty songs (e.g., instrumentals)
    texts = df[df["lemmas"].str.strip() != ""]["lemmas"].tolist()
    valid_songs = df[df["lemmas"].str.strip() != ""]["song"].tolist()
    
    matrix, features = build_tfidf_matrix(texts)
    nmf_model = build_nmf_model(matrix, n_topics=args.topics)
    
    results = {
        "topics": get_topic_words(nmf_model, features),
        "song_mapping": dict(zip(valid_songs, get_song_topics(nmf_model, matrix)))
    }
    save_analysis(results, args.band)

if __name__ == "__main__":
    main()