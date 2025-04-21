# play song by uri


from auth import SpotipyClient
from sp_mcp import mcp


@mcp.tool(name="play_song_by_uri")
def play_song_by_uri(uri: str) -> None:
    auth = SpotipyClient()
    sp = auth.sp
    sp.start_playback(uris=[f"spotify:track:{uri}"])
    return None


if __name__ == "__main__":
    print(play_song_by_uri(uri="0HmmGtJzwfqvpKW0ixeapq"))
