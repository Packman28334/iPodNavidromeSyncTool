
import track_manager

from textual import log
from textual.app import ComposeResult
from textual.widgets import SelectionList, Input, ProgressBar
from textual.containers import Vertical
from textual.reactive import reactive
from textual.css.query import NoMatches

from typing import Literal

class MediaPane(Vertical):

    CSS_PATH = "media_pane.tcss"

    search_value: str = reactive("")

    def __init__(self, which: Literal["track"] | Literal["album"] | Literal["artist"] | Literal["playlist"]):
        super().__init__()
        self.which: Literal["track"] | Literal["album"] | Literal["artist"] | Literal["playlist"] = which

    def get_options(self) -> list[tuple]:
        match self.which:
            case "track":
                return [(str(track), track, track.explicit_flag_for_ipod) for track in track_manager.track_list if self.search_value in str(track).lower()]
            case "album":
                return [(f"{album[0]} ({album[1]})", album, album in track_manager.selected_albums) for album in track_manager.album_list if self.search_value in f"{album[0]} ({album[1]})".lower()]
            case "artist":
                return [(artist, artist, artist in track_manager.selected_artists) for artist in track_manager.artist_list if self.search_value in artist.lower()]
            case "playlist":
                return [(playlist, playlist, playlist in track_manager.selected_playlists) for playlist in track_manager.playlist_list if self.search_value in playlist.lower()]

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
        
    def on_selection_list_selected_changed(self, changed: SelectionList.SelectedChanged) -> None:
        match self.which:
            case "track":
                for option in self.get_options():
                    option[1].explicit_flag_for_ipod = option[1] in changed.selection_list.selected
            case "album":
                for option in self.get_options():
                    if option[1] in changed.selection_list.selected and option[1] not in track_manager.selected_albums:
                        track_manager.selected_albums.append(option[1])
                    elif option[1] not in changed.selection_list.selected and option[1] in track_manager.selected_albums:
                        track_manager.selected_albums.remove(option[1])
            case "artist":
                for option in self.get_options():
                    if option[1] in changed.selection_list.selected and option[1] not in track_manager.selected_artists:
                        track_manager.selected_artists.append(option[1])
                    elif option[1] not in changed.selection_list.selected and option[1] in track_manager.selected_artists:
                        track_manager.selected_artists.remove(option[1])
            case "playlist":
                for option in self.get_options():
                    if option[1] in changed.selection_list.selected and option[1] not in track_manager.selected_playlists:
                        track_manager.selected_playlists.append(option[1])
                    elif option[1] not in changed.selection_list.selected and option[1] in track_manager.selected_playlists:
                        track_manager.selected_playlists.remove(option[1])
        self.parent.parent.parent.parent.parent.query_one(ProgressBar).update(total=track_manager.ipod.get_total_space_on_ipod(), progress=track_manager.find_tracks_to_sync())
