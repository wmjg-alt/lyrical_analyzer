import argparse
import json
from pathlib import Path
from dotenv import load_dotenv
from src.utils.file_utils import create_directory, clean_filename, save_text_file, build_band_dir_path
from src.utils.api_utils import get_genius_client, fetch_artist_data, extract_lyrics_from_song
from src.utils.meta_utils import extract_metadata_from_dict

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments for data collection."""
    parser = argparse.ArgumentParser(description="Fetch band lyrics and metadata.")
    parser.add_argument("--band", type=str, required=True, help="Name of the band.")
    parser.add_argument("--max_songs", type=int, default=50, help="Max songs to fetch.")
    return parser.parse_args()

def process_and_save_songs(artist, band_dir: Path, meta_dir: Path, band_name: str) -> None:
    """Iterate through artist songs, save lyrics to files, and export metadata."""
    metadata = {}
    for song in artist.songs:
        lyrics = extract_lyrics_from_song(song)
        safe_title = clean_filename(song.title)
        save_text_file(lyrics, band_dir / f"{safe_title}.txt")
        metadata[safe_title] = extract_metadata_from_dict(song.to_dict())
        
    with open(meta_dir / f"{clean_filename(band_name)}_meta.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

def main() -> None:
    """Execute the data collection pipeline."""
    load_dotenv()
    args = parse_arguments()
    
    band_dir = build_band_dir_path("data", args.band)
    meta_dir = Path("data") / "metadata"
    create_directory(band_dir)
    create_directory(meta_dir)
    
    client = get_genius_client()
    artist = fetch_artist_data(client, args.band, args.max_songs)
    if artist:
        process_and_save_songs(artist, band_dir, meta_dir, args.band)

if __name__ == "__main__":
    main()