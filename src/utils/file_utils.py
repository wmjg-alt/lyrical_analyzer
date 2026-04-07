import re
from pathlib import Path

def create_directory(path: Path) -> None:
    """Create a directory if it does not exist."""
    path.mkdir(parents=True, exist_ok=True)

def clean_filename(name: str) -> str:
    """Format string into a safe, lowercase filesystem name."""
    # Remove illegal chars, strip lingering edge whitespace, then replace inner spaces
    cleaned = re.sub(r'[\\/*?:"<>|]', "", name).strip()
    return cleaned.replace(" ", "_").lower()

def save_text_file(content: str, file_path: Path) -> None:
    """Write string content to a specified text file."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

def build_band_dir_path(base_dir: str, band_name: str) -> Path:
    """Construct and return the Path object for a band's raw data directory."""
    safe_band_name = clean_filename(band_name)
    return Path(base_dir) / "raw" / safe_band_name