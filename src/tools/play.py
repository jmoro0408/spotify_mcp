from auth import SpotipyClient
from server import mcp


@mcp.tool(name="play_song_by_uri")
def play_song_by_uri(uri: str) -> None:
    auth = SpotipyClient()
    sp = auth.sp
    sp.start_playback(uris=[f"spotify:track:{uri}"])
    return None
