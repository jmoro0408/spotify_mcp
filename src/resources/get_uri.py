from auth import SpotipyClient
from server import mcp


@mcp.resource("play://{artist}_{song}")  # how to name this?
def get_uri_from_artist_song(artist: str, song: str) -> str | None:
    auth = SpotipyClient()
    sp = auth.sp
    query = f"artist:{artist} track:{song}"
    results = sp.search(q=query, type="track", limit=1)
    if results is None:
        return None
    tracks = results["tracks"]["items"]
    if tracks:
        return tracks[0]["uri"]
    else:
        return None
