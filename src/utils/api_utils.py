import os
import lyricsgenius

def get_genius_client() -> lyricsgenius.Genius:
    """Initialize and return the Genius API client with polite rate limiting and browser spoofing."""
    token = os.getenv("GENIUS_ACCESS_TOKEN")
    if not token:
        raise ValueError("GENIUS_ACCESS_TOKEN environment variable not set.")
    
    # Initialize the client
    client = lyricsgenius.Genius(token, sleep_time=2.5, retries=3)
    
    # Bypass Cloudflare 403 Forbidden by spoofing a standard web browser User-Agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    client._session.headers.update(headers)
    
    client.remove_section_headers = True
    return client

def fetch_artist_data(client: lyricsgenius.Genius, band_name: str, max_songs: int):
    """Retrieve artist object containing songs from Genius."""
    return client.search_artist(band_name, max_songs=max_songs, sort="popularity")

def extract_lyrics_from_song(song) -> str:
    """Extract and format lyrics from a single song object."""
    return song.lyrics if song.lyrics else ""