# server.py
from mcp.server.fastmcp import FastMCP

from auth import SpotipyClient
from utils import strip_uri

# Create an MCP server
mcp = FastMCP("Spotify_MCP")


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


@mcp.tool(name="play_song_by_uri")
def play_song_by_uri(uri: str) -> None:
    uri = strip_uri(uri)
    auth = SpotipyClient()
    sp = auth.sp
    sp.start_playback(uris=[f"spotify:track:{uri}"])
    return None


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
