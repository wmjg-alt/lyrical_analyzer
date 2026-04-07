from src.utils.meta_utils import extract_metadata_from_dict

def test_extract_metadata_valid() -> None:
    """Verify year, pageviews, and album are extracted."""
    mock_data = {
        "release_date_components": {"year": 2001},
        "stats": {"pageviews": 1500000},
        "album": {"name": "Toxicity"}
    }
    result = extract_metadata_from_dict(mock_data)
    assert result["year"] == 2001
    assert result["pageviews"] == 1500000
    assert result["album"] == "Toxicity"

def test_extract_metadata_missing() -> None:
    """Verify missing data is handled gracefully."""
    result = extract_metadata_from_dict({})
    assert result["year"] is None
    assert result["album"] is None