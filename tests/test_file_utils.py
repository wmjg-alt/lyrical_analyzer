from pathlib import Path
from src.utils.file_utils import clean_filename, build_band_dir_path

def test_clean_filename() -> None:
    """Verify illegal characters are removed and spaces become underscores."""
    raw_name = 'System of a Down: "Toxicity" /\\?'
    expected = "system_of_a_down_toxicity"
    assert clean_filename(raw_name) == expected

def test_build_band_dir_path() -> None:
    """Verify correct path construction for band data."""
    base = "data"
    band = "System of a Down"
    expected = Path("data/raw/system_of_a_down")
    assert build_band_dir_path(base, band) == expected