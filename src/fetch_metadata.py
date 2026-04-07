import argparse
import json
from pathlib import Path
from src.utils.api_utils import get_genius_client
from src.utils.file_utils import clean_filename, create_directory
from src.utils.meta_utils import fetch_song_metadata
from dotenv import load_dotenv

def parse_meta_args() -> argparse.Namespace:
    """Parse command-line arguments for metadata fetching."""
    parser = argparse.ArgumentParser(description="Fetch song metadata.")
    parser.add_argument("--band", type=str, required=True, help="Name of the band.")
    return parser.parse_args()

def load_song_list(band: str) -> list[str]:
    """Load the list of valid processed songs for a band."""
    file_path = Path("data") / "processed" / f"{clean_filename(band)}_processed.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return [item["song"] for item in json.load(f)]

def save_metadata(data: dict, band: str) -> None:
    """Save the metadata dictionary to JSON."""
    out_dir = Path("data") / "metadata"
    create_directory(out_dir)
    safe_band = clean_filename(band)
    with open(out_dir / f"{safe_band}_meta.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main() -> None:
    """Execute the metadata enrichment pipeline."""
    load_dotenv()
    
    args = parse_meta_args()
    client = get_genius_client()
    songs = load_song_list(args.band)
    
    metadata = {}
    for song_title in songs:
        metadata[song_title] = fetch_song_metadata(client, song_title, args.band)
        
    save_metadata(metadata, args.band)

if __name__ == "__main__":
    main()