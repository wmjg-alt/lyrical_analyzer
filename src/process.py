import argparse
import pandas as pd
from pathlib import Path
from src.utils.nlp_utils import load_nlp_model, clean_raw_lyrics, extract_lemmas
from src.utils.file_utils import clean_filename, create_directory

def parse_process_args() -> argparse.Namespace:
    """Parse command-line arguments for NLP processing."""
    parser = argparse.ArgumentParser(description="Process raw lyrics.")
    parser.add_argument("--band", type=str, required=True, help="Name of the band.")
    return parser.parse_args()

def process_song_file(file_path: Path, nlp) -> dict:
    """Read, clean, and extract NLP lemmas from a single song file."""
    raw_text = file_path.read_text(encoding="utf-8")
    cleaned_text = clean_raw_lyrics(raw_text)
    lemmas = extract_lemmas(nlp(cleaned_text))
    return {"song": file_path.stem, "lemmas": " ".join(lemmas)}

def process_band_directory(band_dir: Path, nlp) -> list[dict]:
    """Process all text files in a band's directory."""
    return [process_song_file(p, nlp) for p in band_dir.glob("*.txt")]

def save_processed_data(data: list[dict], band: str) -> None:
    """Save processed song dictionaries to a JSON file."""
    out_dir = Path("data") / "processed"
    create_directory(out_dir)
    df = pd.DataFrame(data)
    safe_band = clean_filename(band)
    df.to_json(out_dir / f"{safe_band}_processed.json", orient="records", indent=2)

def main() -> None:
    """Execute the NLP processing pipeline."""
    args = parse_process_args()
    band_dir = Path("data") / "raw" / clean_filename(args.band)
    nlp = load_nlp_model()
    data = process_band_directory(band_dir, nlp)
    save_processed_data(data, args.band)

if __name__ == "__main__":
    main()