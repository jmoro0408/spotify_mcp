from mcp.server.fastmcp import FastMCP

from auth import SpotipyClient
from resources import _get_uri_from_artist_song
from tools import _play_song_by_uri

mcp = FastMCP("Spotify_MCP")

client = SpotipyClient()


@mcp.resource("play://{artist}_{song}")
def get_uri_from_artist_song(artist: str, song: str) -> str | None:
    return _get_uri_from_artist_song(artist, song)


@mcp.tool(name="play_song_by_uri")
def play_song_by_uri(uri: str) -> bool:
    return _play_song_by_uri(uri)


if __name__ == "__main__":
    mcp.run(transport="stdio")
