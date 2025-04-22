from mcp.server.fastmcp import FastMCP

from resources import _get_uri_from_artist_song, _get_user_playlists
from tools import (
    _get_currently_playing,
    _list_user_playlists,
    _play_song_by_artist,
    _play_song_by_uri,
)

mcp = FastMCP("Spotify_MCP")

# Resources


@mcp.resource(
    "play://{artist}_{song}",
    name="get_uri_from_artist_song",
    description="get unique spotify uri from artist and song",
)
def get_uri_from_artist_song(artist: str, song: str) -> str | None:
    return _get_uri_from_artist_song(artist, song)


@mcp.resource(
    "read://playlists",
    name="get_user_playlists",
    description="get user playlists",
)
def get_user_playlists() -> list[str]:
    return _get_user_playlists()


# Tools


@mcp.tool(
    name="get_currently_playing",
    description="get the currently playing artist and song",
)
def get_currently_playing() -> str | None:
    return _get_currently_playing()


@mcp.tool(
    name="play_song_by_uri", description="play a song on spotify given its unique uri"
)
def play_song_by_uri(uri: str) -> bool:
    return _play_song_by_uri(uri)


@mcp.tool(
    name="play_song_by_artist_song",
    description="play a song on spotify given its artist and song",
)
def play_song_by_artist(artist: str, song: str) -> bool:
    return _play_song_by_artist(artist=artist, song=song)


@mcp.tool(
    name="get_user_playlists",
    description="list the users playlists",
)
def list_user_playlists() -> str:
    return _list_user_playlists()


if __name__ == "__main__":
    mcp.run(transport="stdio")
