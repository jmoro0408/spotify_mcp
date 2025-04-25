from pathlib import Path

import spotipy
from dotenv import find_dotenv, load_dotenv
from spotipy.oauth2 import SpotifyOAuth


class SpotipyClient:
    def __init__(self):
        load_dotenv(find_dotenv())
        scope = [
            "user-library-read",
            "user-read-playback-state",
            "user-modify-playback-state",
            "user-read-currently-playing",
            "playlist-read-private",
            "playlist-read-collaborative",
            "user-read-recently-played",
        ]
        cache_path = Path(Path.home(), ".spotify_mcp_cache")
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(scope=scope, cache_path=cache_path)
        )


client = SpotipyClient()
