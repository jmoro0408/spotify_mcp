# server.py
from mcp.server.fastmcp import FastMCP

from auth import SpotipyClient
from utils import strip_uri

mcp = FastMCP("Spotify_MCP")

client = SpotipyClient()


@mcp.resource("play://{artist}_{song}")  # how to name this?
def get_uri_from_artist_song(artist: str, song: str) -> str | None:
    sp = client.sp
    query = f"artist:{artist} track:{song}"
    results = sp.search(q=query, type="track", limit=1)
    if results is None:
        return None
    tracks = results["tracks"]["items"]

    if tracks:
        return tracks[0]["uri"]
    else:
        return None


@mcp.tool(name="play_song_by_uri")
def play_song_by_uri(uri: str) -> None:
    uri = strip_uri(uri)

    sp = client.sp
    sp.start_playback(uris=[f"spotify:track:{uri}"])
    return None


if __name__ == "__main__":
    mcp.run(transport="stdio")
