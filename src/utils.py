import re


def strip_uri(uri: str) -> str:
    return re.sub(r"spotify:track:", "", uri)
