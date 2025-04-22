import difflib

from auth import client
from utils import logger


def _get_uri_from_artist_song(artist: str, song: str) -> str | None:
    try:
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
    except Exception as e:
        logger.error(f"Failed to get uri from artist and song: {str(e)}")
        raise


def get_all_user_playlists():
    all_playlists = []
    sp = client.sp
    results = sp.current_user_playlists(limit=50)
    while results:
        all_playlists.extend(results["items"])
        if results["next"]:
            results = sp.next(results)
        else:
            break
    return all_playlists


def _get_user_playlists() -> list[str]:
    try:
        playlists = get_all_user_playlists()
        if playlists is None:
            return []
        return [x["name"] for x in playlists]

    except Exception as e:
        logger.error(f"Failed to get user playlists: {str(e)}")
        raise


def _get_user_playlist_id(
    playlist_name: str, similarity_threshold: float = 0.6
) -> str | None:
    sp = client.sp

    all_playlists = []
    results = sp.current_user_playlists()
    while results:
        all_playlists.extend(results["items"])
        if results["next"]:
            results = sp.next(results)
        else:
            break

    playlist_names = [p["name"] for p in all_playlists]

    matches = difflib.get_close_matches(
        playlist_name, playlist_names, n=1, cutoff=similarity_threshold
    )

    if matches:
        best_match = matches[0]
        playlist = next(p for p in all_playlists if p["name"] == best_match)
        return playlist["id"]
    else:
        logger.error("Playlist ID not found.")
        return None


if __name__ == "__main__":
    print(get_all_user_playlists())
    print(len(get_all_user_playlists()))
