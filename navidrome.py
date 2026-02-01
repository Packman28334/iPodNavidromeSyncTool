import os
from dotenv import load_dotenv
load_dotenv()

import requests

def send_get_request(endpoint: str, params: dict = {}):
    base_url: str = f"{os.environ['NAVIDROME_URL']}{endpoint}?u={os.environ['NAVIDROME_USERNAME']}&p={os.environ['NAVIDROME_PASSWORD']}&v=1.13.0&c=iPodSyncTool&f=json"
    r = requests.get(
        base_url+"&"+"&".join([key+"="+str(value) for key, value in params.items()]) if params else base_url
    )
    return r.json()

def get_tracks() -> list[dict]:
    tracks: list[dict] = []
    page: int = 0
    while True:
        tracks.extend([{
                "title": track["title"],
                "artist": track["artist"],
                "album": track["album"],
                "genre": track["genre"] if "genre" in track else "",
                "year": track["year"] if "year" in track else 0,
                "track_number": track["track"] if "track" in track else 1,
                "navidrome_id": track["id"],
                "size": track["size"]
            } for track in send_get_request("/rest/search3", {"query": "", "artistCount": 0, "albumCount": 0, "songCount": 1000, "songOffset": 1000*page})["subsonic-response"]["searchResult3"]["song"]])
        page += 1
        if len(tracks) % 1000: # if we're at the end (we didn't return a full 1000 song page), break
            break
    return tracks