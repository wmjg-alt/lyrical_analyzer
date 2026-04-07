import json
from unittest.mock import MagicMock
from pathlib import Path
from src.collect import process_and_save_songs

def test_process_and_save_songs(tmp_path: Path) -> None:
    """Verify lyrics and metadata are correctly routed and saved."""
    mock_artist = MagicMock()
    mock_song = MagicMock()
    mock_song.lyrics = "Sample lyrics"
    mock_song.title = "Test Song"
    mock_song.to_dict.return_value = {"release_date_components": {"year": 2001}}
    mock_artist.songs =[mock_song]
    
    band_dir = tmp_path / "raw"
    meta_dir = tmp_path / "meta"
    band_dir.mkdir()
    meta_dir.mkdir()
    
    process_and_save_songs(mock_artist, band_dir, meta_dir, "Test Band")
    
    assert (band_dir / "test_song.txt").read_text() == "Sample lyrics"
    meta_data = json.loads((meta_dir / "test_band_meta.json").read_text())
    assert meta_data["test_song"]["year"] == 2001