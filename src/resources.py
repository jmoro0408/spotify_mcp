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


def _get_user_playlists() -> list[str]:
    try:
        sp = client.sp
        playlists = sp.current_user_playlists()
        if playlists is None or "items" not in playlists:
            return []
        return [x["name"] for x in playlists["items"]]

    except Exception as e:
        logger.error(f"Failed to get user playlists: {str(e)}")
        raise


if __name__ == "__main__":
    print(_get_user_playlists())
