import lyricsgenius

def extract_metadata_from_dict(song_dict: dict) -> dict:
    """Extract year, pageviews, and album from a Genius song dictionary."""
    year = None
    date_comps = song_dict.get("release_date_components")
    if isinstance(date_comps, dict):
        year = date_comps.get("year")
        
    stats = song_dict.get("stats", {})
    album = song_dict.get("album")
    album_name = album.get("name") if isinstance(album, dict) else None
    
    return {"year": year, "pageviews": stats.get("pageviews"), "album": album_name}

def fetch_song_metadata(client: lyricsgenius.Genius, title: str, artist: str) -> dict:
    """Fetch and extract metadata for a single song."""
    song = client.search_song(title, artist)
    if not song:
        return {"year": None, "pageviews": None, "album": None}
    return extract_metadata_from_dict(song.to_dict())