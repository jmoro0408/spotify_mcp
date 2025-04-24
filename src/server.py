from mcp.server.fastmcp import FastMCP

from resources import _get_uri_from_artist_song, _get_user_playlists
from tools import (
    _get_currently_playing,
    _get_playlist_id,
    _list_user_playlists,
    _next_track,
    _pause_playback,
    _play_playlist_by_id,
    _play_song_by_artist,
    _play_song_by_uri,
    _play_user_liked_songs,
    _play_user_playlist_by_name,
    _previous_track,
    _start_playback,
    _turn_shuffle_off,
    _turn_shuffle_on,
)

mcp = FastMCP("Spotify_MCP")

# Resources


@mcp.resource(
    "play://{artist}_{song}",
    name="get_uri_from_artist_song",
    description="get unique spotify uri from artist and song",
)
def get_uri_from_artist_song(artist: str, song: str) -> str | None:
    """
    Get the unique Spotify URI for a given artist and song.

    Args:
        artist (str): The name of the artist.
        song (str): The name of the song.

    Returns:
        str | None: The Spotify URI if found, otherwise None.
    """

    return _get_uri_from_artist_song(artist, song)


@mcp.resource(
    "read://playlists",
    name="get_user_playlists",
    description="get user playlists",
)
def get_user_playlists() -> list[str]:
    """
    Get a list of the names of the user's playlists.

    Returns:
        list[str]: A list of the names of the user's playlists.
    """
    return _get_user_playlists()


# Tools


@mcp.tool(
    name="get_currently_playing",
    description="get the currently playing artist and song",
)
def get_currently_playing() -> str | None:
    """
    Get the currently playing artist and song.

    Returns:
        str | None: The currently playing artist and song if a track is
            currently playing, otherwise None.
    """
    return _get_currently_playing()


@mcp.tool(
    name="play_song_by_uri", description="play a song on spotify given its unique uri"
)
def play_song_by_uri(uri: str) -> bool:
    """
    Play a song on Spotify using its unique URI.

    Args:
        uri (str): The unique Spotify URI of the song to play.

    Returns:
        bool: True if the song was successfully played, False otherwise.
    """

    return _play_song_by_uri(uri)


@mcp.tool(
    name="play_song_by_artist_song",
    description="play a song on spotify given its artist and song",
)
def play_song_by_artist(artist: str, song: str) -> bool:
    """
    Play a song on Spotify using its artist and song name.

    Args:
        artist (str): The name of the artist of the song to play.
        song (str): The name of the song to play.

    Returns:
        bool: True if the song was successfully played, False otherwise.
    """
    return _play_song_by_artist(artist=artist, song=song)


@mcp.tool(
    name="get_user_playlists",
    description="list the users playlists",
)
def list_user_playlists() -> str:
    """
    List the names of the user's playlists in a comma-separated string.

    Returns:
        str: A comma-separated string of the user's playlist names.
    """

    return _list_user_playlists()


@mcp.tool(
    name="play_user_playlist_by_name",
    description="play a user's playlist given its name",
)
def play_user_playlist_by_name(playlist_name: str) -> bool:
    """
    Play a user's playlist by its name.

    Args:
        playlist_name (str): The name of the user's playlist to play.

    Returns:
        bool: True if the playlist was successfully played, False otherwise.
    """

    return _play_user_playlist_by_name(playlist_name)


@mcp.tool(
    name="play_public_playlist_by_name",
    description="play a public playlist given it's name",
)
def play_public_playlist_by_name(playlist_name: str) -> bool:
    """
    Play a public playlist on Spotify using its name.

    Args:
        playlist_name (str): The name of the public playlist to play.

    Returns:
        bool: True if the playlist was successfully played, False otherwise.
    """
    playlist_id = _get_playlist_id(playlist_name)
    if playlist_id:
        return _play_playlist_by_id(playlist_id)
    else:
        return False


@mcp.tool(
    name="pause_playback",
    description="pause playback on active device",
)
def pause_playback() -> bool:
    """
    Pause playback on the active device.

    Returns:
        bool: True if the playback was successfully paused, False otherwise.
    """
    return _pause_playback()


@mcp.tool(
    name="start_playback",
    description="start playback on active device",
)
def start_playback() -> bool:
    """
    Start playback on the active device.

    Returns:
        bool: True if the playback was successfully started, False otherwise.
    """
    return _start_playback()


@mcp.tool(
    name="next_track",
    description="skip to next track on active device",
)
def next_track() -> bool:
    """
    Skip to the next track on the active device.

    Returns:
        bool: True if the track was successfully skipped, False otherwise.
    """
    return _next_track()


@mcp.tool(
    name="previous_track",
    description="skip to previous track on active device",
)
def previous_track() -> bool:
    """
    Skip to the previous track on the active device.

    Returns:
        bool: True if the track was successfully skipped, False otherwise.
    """
    return _previous_track()


@mcp.tool(
    name="turn_shuffle_on",
    description="Toggle shuffle on active device",
)
def turn_shuffle_on() -> bool:
    """
    Toggle shuffle on the active device.

    Returns:
        bool: True if shuffle was successfully enabled, False otherwise.
    """
    return _turn_shuffle_on()


@mcp.tool(
    name="turn_shuffle_off",
    description="Toggle shuffle off active device",
)
def turn_shuffle_off() -> bool:
    """
    Toggle shuffle off on the active device.

    Returns:
        bool: True if shuffle was successfully disabled, False otherwise.
    """
    return _turn_shuffle_off()


@mcp.tool(
    name="play_user_liked_songs",
    description="Play the user's liked songs",
)
def play_user_liked_songs() -> bool:
    """
    Play the user's liked songs.

    Returns:
        bool: True if the tracks were successfully played, False otherwise.
    """
    return _play_user_liked_songs()


if __name__ == "__main__":
    mcp.run(transport="stdio")
