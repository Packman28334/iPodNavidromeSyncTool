
import ipod
import navidrome

import os
import json
from pathlib import Path

class Track:
    def __init__(self, title: str, artist: str, album: str, genre: str, year: int, track_number: int, size: int, navidrome_id: str):
        self.title: str = title
        self.artist: str = artist
        self.album: str = album
        self.genre: str = genre
        self.year: int = year
        self.track_number: int = track_number
        self.size: int = size
        self.navidrome_id: str = navidrome_id
        
        self.is_on_ipod: bool = False # on iPod right now?
        self.explicit_flag_for_ipod: bool = False # user requested this song specifically to be on the iPod
        self.implicit_flag_for_ipod: bool = False # this song should be on the iPod because of other user requests (artist/album/playlist)

    def create_ipod_track(self) -> ipod.gpod.Track:
        ipod_track: ipod.gpod.Track = ipod.gpod.Track(
            title=self.title,
            artist=self.artist,
            album=self.album,
            genre=self.genre
        )
        ipod_track.year = self.year
        ipod_track.track_number = self.track_number
        return ipod_track

    def match_with_ipod_track(self, track: ipod.gpod.Track) -> bool:
        return self.title == track.title and self.artist == track.artist and self.album == track.album # and self.genre == track.genre and self.year == track.year and self.track_number == track.track_number

    def dump(self) -> dict:
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "genre": self.genre,
            "year": self.year,
            "track_number": self.track_number,
            "size": self.size,
            "navidrome_id": self.navidrome_id
        }
    
    def match_with_track_dump(self, data: dict) -> bool:
        return self.title == data["title"] and self.artist == data["artist"] and self.album == data["album"] and self.genre == data["genre"] and self.year == data["year"] and self.track_number == data["track_number"]

    def __str__(self):
        return f"{self.title} | {self.album} | {self.artist}"

    def __repr__(self):
        return f"Track(title='{self.title}', artist='{self.artist}', album='{self.album}', genre='{self.genre}', year={self.year}, track_number={self.track_number}, size={self.size}, navidrome_id='{self.navidrome_id}')"

album_list: list[tuple[str, str]] = navidrome.get_albums()
artist_list: list[str] = navidrome.get_artists()
playlist_list: list[str] = []

track_list: list[Track] = [Track(**navidrome_track) for navidrome_track in navidrome.get_tracks()]
unmatched_ipod_tracks: list[ipod.gpod.Track] = []

for ipod_track in ipod.db.tracks:
    navidrome_match_found: bool = False
    for track in track_list:
        if track.match_with_ipod_track(ipod_track):
            navidrome_match_found = True
            track.is_on_ipod = True
            continue
    if not navidrome_match_found:
        unmatched_ipod_tracks.append(ipod_track)

selected_albums: list[tuple[str, str]] = []
selected_artists: list[str] = []
selected_playlists: list[str] = []

if os.path.exists("selections.json"):
    json_data: dict = json.loads(Path("selections.json").read_text())
    for selected_track in json_data["tracks"]:
        for track in track_list:
            if track.match_with_track_dump(selected_track):
                track.explicit_flag_for_ipod = True
    for album in json_data["albums"]:
        selected_albums.append((album[0], album[1]))
    selected_artists: list[str] = json_data["artists"]
    selected_playlists: list[str] = json_data["playlists"]

def save_previously_selected() -> None:
    Path("selections.json").write_text(json.dumps({
        "tracks": [track.dump() for track in track_list if track.explicit_flag_for_ipod],
        "albums": [[album[0], album[1]] for album in selected_albums],
        "artists": selected_artists,
        "playlists": selected_playlists
    }))

def find_tracks_to_sync() -> int:
    for track in track_list:
        track.implicit_flag_for_ipod = (track.album, track.artist) in selected_albums or track.artist in selected_artists
    total_size: int = 0
    for track in track_list:
        if track.explicit_flag_for_ipod or track.implicit_flag_for_ipod:
            total_size += track.size
    return total_size

def synchronize() -> str:
    tracks_to_add: list[Track] = [track for track in track_list if (track.implicit_flag_for_ipod or track.explicit_flag_for_ipod) and not track.is_on_ipod]
    tracks_to_remove: list[ipod.gpod.Track] = [track.create_ipod_track() for track in track_list if not (track.implicit_flag_for_ipod or track.explicit_flag_for_ipod) and track.is_on_ipod]
    tracks_to_remove.extend(unmatched_ipod_tracks)

    print(tracks_to_add)
    print(tracks_to_remove)

    for track in tracks_to_add:
        print(f"SYNCING {str(track)}")
        ipod_track: ipod.gpod.Track = track.create_ipod_track()
        navidrome.download_track(track.navidrome_id)
        success: bool = ipod.db.copy_file_to_ipod(ipod_track, "track.m4a")
        if success:
            ipod.db.add(ipod_track)
            ipod.db.save()
    
    print("SYNC DONE")