
import ipod
import navidrome

class Track:
    def __init__(self, title: str, artist: str, album: str, genre: str, year: int, track_number: int, size: int, navidrome_id: str, is_on_ipod: bool = False):
        self.title: str = title
        self.artist: str = artist
        self.album: str = album
        self.genre: str = genre
        self.year: int = year
        self.track_number: int = track_number
        self.size: int = size
        self.navidrome_id: str = navidrome_id
        self.is_on_ipod: bool = is_on_ipod

    def match_with_ipod_track(self, track: ipod.gpod.Track) -> bool:
        return self.title == track.title and self.artist == track.artist and self.album == track.album # and self.genre == track.genre and self.year == track.year and self.track_number == track.track_number

    def __str__(self):
        return f"{self.title} | {self.album} | {self.artist}"

    def __repr__(self):
        return f"Track(title='{self.title}', artist='{self.artist}', album='{self.album}', genre='{self.genre}', year={self.year}, track_number={self.track_number}, size={self.size}, navidrome_id='{self.navidrome_id}', is_on_ipod={self.is_on_ipod})"

def load_track_listings() -> tuple[list[Track], list[ipod.gpod.Track]]:
    tracks: list[Track] = [Track(**navidrome_track) for navidrome_track in navidrome.get_tracks()]
    unmatched_ipod_tracks: list[ipod.gpod.Track] = []
    for ipod_track in ipod.db.tracks:
        navidrome_match_found: bool = False
        for track in tracks:
            if track.match_with_ipod_track(ipod_track):
                navidrome_match_found = True
                track.is_on_ipod = True
                continue
        if not navidrome_match_found:
            unmatched_ipod_tracks.append(ipod_track)
    return tracks, unmatched_ipod_tracks