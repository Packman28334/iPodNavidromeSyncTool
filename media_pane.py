
import track_manager

from textual import log
from textual.app import ComposeResult
from textual.widgets import SelectionList, Input
from textual.containers import Vertical
from textual.reactive import reactive
from textual.css.query import NoMatches

from typing import Literal

class MediaPane(Vertical):

    CSS_PATH = "media_pane.tcss"

    search_value: str = reactive("")

    def __init__(self, track_list: list[track_manager.Track], album_list: list[tuple[str, str]], artist_list: list[str], playlist_list: list[str], which: Literal["track"] | Literal["album"] | Literal["artist"] | Literal["playlist"]):
        super().__init__()
        self.track_list: list[track_manager.Track] = track_list
        self.album_list: list[tuple[str, str]] = album_list
        self.artist_list: list[str] = artist_list
        self.playlist_list: list[str] = playlist_list
        self.which: Literal["track"] | Literal["album"] | Literal["artist"] | Literal["playlist"] = which

    def get_options(self) -> list[tuple]:
        match self.which:
            case "track":
                return [(str(track), track) for track in self.track_list if self.search_value in str(track).lower()]
            case "album":
                return [(f"{album[0]} ({album[1]})", album) for album in self.album_list if self.search_value in f"{album[0]} ({album[1]})".lower()]
            case "artist":
                return [(artist, artist) for artist in self.artist_list if self.search_value in artist.lower()]
            case "playlist":
                return [(playlist, playlist) for playlist in self.playlist_list if self.search_value in playlist.lower()]

    def compose(self) -> ComposeResult:
        yield Input(value=self.search_value, placeholder="Search...")
        match self.which:
            case "track":
                yield SelectionList[track_manager.Track](*self.get_options())
            case "album":
                yield SelectionList[tuple[str, str]](*self.get_options())
            case "artist":
                yield SelectionList[str](*self.get_options())
            case "playlist":
                yield SelectionList[str](*self.get_options())
    
    def on_input_changed(self, changed: Input.Changed) -> None:
        self.search_value = changed.value.lower()

    def watch_search_value(self, search_value: str) -> None:
        try:
            self.query_one(SelectionList).clear_options()
            self.query_one(SelectionList).add_options(self.get_options())
        except NoMatches:
            return